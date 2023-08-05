# Copyright 2021 Q-CTRL Pty Ltd & Q-CTRL Inc. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

"""
Module for converting Q-CTRL optimized pulses into QUA configurations.
"""

import json
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

import numpy as np


def qctrl_pulse_to_samples(
    qctrl_pulse: List[Dict[str, Union[float, complex]]],
    rabi_to_amplitude_func: Optional[
        Callable[[float, float], Tuple[float, float]]
    ] = None,
    max_amplitude: float = 0.4,
) -> Tuple[List[float], List[float]]:
    """
    Converts a pulse in Q-CTRL optimizer output in dictionary format into
    two lists that you can send to QUA config.

    Parameters
    ----------
    qctrl_pulse : list[dict]
        A list of the numerical values of a pulse waveform. Each element is
        a dict which has two keys, ``duration`` and ``value``. The
        durations are in unit of seconds. The ``value`` can be complex,
        corresponding to I/Q value of the pulse.
    rabi_to_amplitude_func : function, optional
        A function mapping pulse amplitude into unitless numbers. The
        function takes the form
        ``func(x: float, y: float): tuple[float, float]``, accepting as
        input the I/Q values of the pulse in units of Hz, and returning as
        output the unitless value of the I/Q.
    max_amplitude : float, optional
        The maximum pulse amplitude number of the system. The value should
        be between 0.1 and 0.49. If no `rabi_to_amplitude_func` function is
        provided, or the output value goes beyond 0.49, the output values
        scaled to a maximum amplitude of `max_amplitude` will be used. By
        default 0.4.

    Returns
    -------
    tuple[list, list]
        The lists of I and Q numerical values (respectively), in 1
        nanosecond sample rate.
    """
    if max_amplitude > 0.49 or max_amplitude < 0.1:
        raise ValueError("max_amplitude must be between 0.1 and 0.49.")

    segments = np.repeat(
        [segment["value"] for segment in qctrl_pulse],
        [np.rint(segment["duration"] / 1e-9) for segment in qctrl_pulse],
    )
    segments = np.pad(segments, (0, 4 - len(segments) % 4))

    segment_i = np.real(segments)
    segment_q = np.imag(segments)
    if rabi_to_amplitude_func is None:
        max_i = np.max(np.abs(segment_i))
        max_q = np.max(np.abs(segment_q))
        max_input = max(max_i, max_q)
        scale_factor = max_input / max_amplitude
        rabi_to_amplitude_func = lambda x, y: (x / scale_factor, y / scale_factor)

    pulse_sample_i, pulse_sample_q = [], []
    for input_i, input_q in zip(segment_i, segment_q):
        output_i, output_q = rabi_to_amplitude_func(input_i, input_q)
        pulse_sample_i.append(output_i)
        pulse_sample_q.append(output_q)

    # Check the input range
    max_output_i = np.max(np.abs(pulse_sample_i))
    max_output_q = np.max(np.abs(pulse_sample_q))
    max_output = max(max_output_i, max_output_q)
    if max_output > max_amplitude:
        # Rescale is needed
        scale_factor = max_output / max_amplitude
        new_pulse_sample_i, new_pulse_sample_q = [], []
        for input_i, input_q in zip(pulse_sample_i, pulse_sample_q):
            output_i, output_q = input_i / scale_factor, input_q / scale_factor
            new_pulse_sample_i.append(output_i)
            new_pulse_sample_q.append(output_q)
        pulse_sample_i, pulse_sample_q = new_pulse_sample_i, new_pulse_sample_q

    return pulse_sample_i, pulse_sample_q


class _Qubit:
    """
    Creates Qubit controller objects for QUA config.

    Attributes
    ----------
    config : dict
        The dictionary containing parameters of the qubit controller.
    name : str
        The name of the qubit.
    mixer_config : dict
        The dictionary containing parameters of the mixer associated with
        the qubit.
    mixer_name : str
        The name of the mixer, by default 'mxr_qb'
    """

    def __init__(
        self,
        lo_frequency,
        intermediate_frequency,
        operations=None,
        name=None,
        controller="con1",
        channel=(1, 2),
        mixer_name="mxr_qb",
        correction=[1.0, 0.0, 0.0, 1.0],
    ):

        self.config = {
            "mixInputs": {
                "I": (controller, channel[0]),
                "Q": (controller, channel[1]),
                "lo_frequency": lo_frequency,
                "mixer": mixer_name,
            },
            "intermediate_frequency": intermediate_frequency,
            "operations": {} if not operations else operations,
        }
        self.mixer_config = [
            {
                "intermediate_frequency": intermediate_frequency,
                "lo_frequency": lo_frequency,
                "correction": correction.copy(),
            },
        ]
        self.mixer_name = mixer_name
        self.name = name

    def add_operation(self, operation_name, pulse_name):
        self.config["operations"][operation_name] = pulse_name


class _Waveform:
    def __init__(self, name, sample, constant=False):
        if constant:
            waveform = {"type": "constant", "sample": sample[0]}
        else:
            waveform = {"type": "arbitrary", "samples": sample}
        self.name = name
        self.config = waveform


def _integration_dictionary(
    integration_weight, pulse_length, rot_phase=-0.3, pad=0, integ_name="integW"
):
    w = integration_weight * np.ones(int(pulse_length // 4 + pad))
    w_i = [np.cos(rot_phase) * w, -np.sin(rot_phase) * w]
    w_q = [np.sin(rot_phase) * w, np.cos(rot_phase) * w]
    config = {
        integ_name
        + "_I": {
            "cosine": w_i[0].tolist(),
            "sine": w_i[1].tolist(),
        },
        integ_name
        + "_Q": {
            "cosine": w_q[0].tolist(),
            "sine": w_q[1].tolist(),
        },
    }
    return config


class Pulse:
    """
    Information related to a pulse applied to a qubit or resonator.

    Parameters
    ----------
    pulse_name : str
        A name to identify the pulse.
    sample : Any
        The samples describing the waveform of the pulse. Takes three
        forms:

          - tuple[float, int] : Associated with a constant pulse. The first
            number is the amplitude and the second number is the length of
            the pulse in nanoseconds.
          - list[float] : Associated with a time-dependent pulse with only
            an I channel. The values in the list give the samples of the I
            channel (at a 1 nanosecond sample rate), and the Q channel is
            set to zero. Tuples and NumPy arrays can be used instead of
            lists.
          - list[list[float], list[float]]: Associated with a
            time-dependent pulse with both I and Q channels. The first
            element in the outer list gives the samples of the I channel
            and the second element gives the samples of the Q channel (both
            at a 1 nanosecond sample rate). Tuples and NumPy arrays can be
            used instead of lists.

    constant : bool, optional
        To determine whether the pulse is constant or not. Defaulted to
        False.
    pulse_type : str, optional
        To determine whether the pulse is used to apply to a qubit or to a
        resonator.  Must be either 'control' or 'measurement'. Defaulted to
        'control'.
    integration_weight : float, optional
        The integration weight used in demodulation. Defaulted to 4.0.
    integ_name : str, optional
        The prefix string of the integration weights. Defaulted to
        'integW'.
    """

    def __init__(
        self,
        pulse_name: str,
        sample,
        constant=False,
        pulse_type="control",
        integration_weight=4.0,
        integ_name="integW",
    ):

        pulse_iq = isinstance(sample, (list, np.ndarray, tuple)) and isinstance(
            sample[0], (list, np.ndarray, tuple)
        )
        if constant:
            pulse_length = sample[1]
        else:
            pulse_length = len(sample[0]) if pulse_iq else len(sample)

        if pulse_iq:
            waveform_i = _Waveform(pulse_name + "_I", sample[0])
            waveform_q = _Waveform(pulse_name + "_Q", sample[1])
        else:
            waveform_i = _Waveform(pulse_name + "_wf", sample, constant=constant)
            waveform_q = _Waveform("wf_zero", (0.0, pulse_length), constant=True)

        self.waveform = (waveform_i, waveform_q)
        self.pulse_name = pulse_name

        if pulse_type not in ["control", "measurement"]:
            raise ValueError(
                "The pulse type must be either 'control' or 'measurement'."
            )

        operation = pulse_type

        self.config = {
            "operation": operation,
            "length": pulse_length,
            "waveforms": {
                "I": waveform_i.name,
                "Q": waveform_q.name,
            },
        }
        if pulse_type == "measurement":
            self.config["integration_weights"] = {
                "integ_w_I": integ_name + "_I",
                "integ_w_Q": integ_name + "_Q",
            }
            integ = _integration_dictionary(
                integration_weight, pulse_length, integ_name=integ_name
            )
            self.integ = integ
            self.config["digital_marker"] = "marker1"


class _Resonator:
    def __init__(
        self,
        lo_frequency,
        intermediate_frequency,
        operations=None,
        name=None,
        controller="con1",
        channel=(5, 6),
        mixer_name="mxr_rr",
        correction=[1.0, 0.0, 0.0, 1.0],
    ):
        self.config = {
            "mixInputs": {
                "I": (controller, channel[0]),
                "Q": (controller, channel[1]),
                "lo_frequency": lo_frequency,
                "mixer": mixer_name,
            },
            "intermediate_frequency": intermediate_frequency,
            "operations": {} if not operations else operations,
            "time_of_flight": 200,
            "smearing": 0,
            "outputs": {"out1": (controller, 1), "out2": (controller, 2)},
        }

        self.mixer_config = [
            {
                "intermediate_frequency": intermediate_frequency,
                "lo_frequency": lo_frequency,
                "correction": correction.copy(),
            },
        ]
        self.name = name

    def add_operation(self, operation_name, pulse_name):
        self.config["operations"][operation_name] = pulse_name


class QmConfig:
    """
    Creates a QUA Config object that contains the config dict.
    Based on the number of qubits, the first 2n control ports are used to
    interact with n qubits and the rest are connected to the resonators.

    Parameters
    ----------
    qubit_lo_frequencies : list[float], optional
        The local oscillation frequencies for each qubit, in Hz.
    qubit_intermediate_frequencies : list[float], optional
        The intermediate frequencies for each qubit, in Hz.
    resonator_lo_frequencies : list[float], optional
        The local oscillation frequencies for each resonator, in Hz.
    resonator_intermediate_frequencies : list[float], optional
        The intermediate frequencies for each resonator, in Hz.
    qubit_names : list[str], optional
        The name of each qubit. If no name is given, the default name of
        the first qubit is ``qubit1``, and second qubit is ``qubit2``, and
        so on.
    resonator_names : list[str], optional
        The name of each resonator. If no name is given, the default name
        of the first resonator is ``rr1``, and second resonator is ``rr2``,
        and so on.
    drive_pulses : dict, optional
        The dictionary for pulses that will later be assigned to qubits.
    measurement_pulses : dict, optional
        The dictionary for pulses that will later be assigned to
        resonators.
    offsets : float, optional
        Offsets of the output signals. Defaulted to 0.1.
    version : int, optional
        The version of the config. Defaulted to 1.
    controller : str, optional
        The name of the controller. Defaulted to 'con1'.

    Attributes
    ----------
    config: dict
        The main config that contains all parameters of the Operator-X
        (OPX).
    """

    def __init__(
        self,
        qubit_lo_frequencies=None,
        qubit_intermediate_frequencies=None,
        resonator_lo_frequencies=None,
        resonator_intermediate_frequencies=None,
        qubit_names=None,
        resonator_names=None,
        drive_pulses=None,
        measurement_pulses=None,
        offsets=0.1,
        version=1,
        controller="con1",
    ):

        if qubit_lo_frequencies is None:
            qubit_lo_frequencies = []
        if qubit_intermediate_frequencies is None:
            qubit_intermediate_frequencies = []
        if resonator_lo_frequencies is None:
            resonator_lo_frequencies = []
        if resonator_intermediate_frequencies is None:
            resonator_intermediate_frequencies = []

        if drive_pulses is None:
            drive_pulses = {}
        if measurement_pulses is None:
            measurement_pulses = {}

        self.qubits = []
        self.resonators = []

        config = {}
        config["version"] = version
        config["controllers"] = {
            controller: {
                "type": "opx1",
                "analog_outputs": {i + 1: {"offset": offsets} for i in range(10)},
                "analog_inputs": {i + 1: {"offset": 0.0} for i in range(10)},
            }
        }

        config["elements"] = {}
        config["mixers"] = {}
        config["pulses"] = {}
        config["waveforms"] = {}
        config["integration_weights"] = {}

        # TODO: This part is temporary. We may need extra work to handle digital_waveforms better.
        config["digital_waveforms"] = {}
        config["digital_waveforms"]["marker1"] = {"samples": [(1, 0), (0, 0)]}

        for pulse_name, sample in drive_pulses.items():
            config["pulses"][pulse_name] = Pulse(
                pulse_name, sample, None, pulse_type="control"
            )

        channel = (1, 2)
        for i in range(len(qubit_lo_frequencies)):
            lo_f = qubit_lo_frequencies[i]
            in_f = qubit_intermediate_frequencies[i]

            mixer_name = "mxr_qb" + str(i + 1)
            element_name = qubit_names[i] if qubit_names else "qubit" + str(i + 1)
            element_qubit = _Qubit(
                lo_f,
                in_f,
                controller=controller,
                name=element_name,
                channel=channel,
                mixer_name=mixer_name,
            )
            for pulse_name in drive_pulses:
                element_qubit.add_operation(pulse_name, pulse_name)
            self.qubits.append(element_qubit)

            config["elements"][element_name] = element_qubit.config
            config["mixers"][mixer_name] = element_qubit.mixer_config

            channel = (channel[0] + 2, channel[1] + 2)

        for i in range(len(resonator_lo_frequencies)):
            lo_f = resonator_lo_frequencies[i]
            in_f = resonator_intermediate_frequencies[i]
            mixer_name = "mxr_rr" + str(i + 1)
            element_name = resonator_names[i] if resonator_names else "rr" + str(i + 1)
            element_resonator = _Resonator(
                lo_f,
                in_f,
                controller=controller,
                name=element_name,
                channel=channel,
                mixer_name=mixer_name,
            )
            for pulse_name in measurement_pulses:
                element_resonator.add_operation(pulse_name, pulse_name)
            self.resonators.append(element_resonator)

            config["elements"][element_name] = element_resonator.config
            config["mixers"][mixer_name] = element_resonator.mixer_config

            channel = (channel[0] + 2, channel[1] + 2)

        self.config = config

    def assign_drive_pulse(self, qubit_index, pulse, operation_name=None):
        """
        Assign a driving pulse to a qubit.

        Parameters
        ----------
        qubit_index : int
            The index of the qubit.
        pulse : qua_config_gen.Pulse
            The Pulse object.
        operation_name : str, optional
            The name of the operation corresponding to the pulse.
            If no name is specified, the name of the pulse will be the
            operation name.
        """

        pulse_name = pulse.pulse_name
        pulse_config = pulse.config
        wf_i, wf_q = pulse.waveform

        self.config["pulses"][pulse_name] = pulse_config
        self.config["waveforms"][wf_i.name] = wf_i.config
        self.config["waveforms"][wf_q.name] = wf_q.config

        qb = self.qubits[qubit_index]

        if not operation_name:
            operation_name = pulse_name
        qb.add_operation(operation_name, pulse_name)
        self.config["elements"][qb.name] = qb.config

    def assign_meas_pulse(self, resonator_index, pulse, operation_name=None):
        """
        Assign a measurement pulse to a qubit.

        Parameters
        ----------
        resonator_index : int
            The index of the resonator.
        pulse : qua_config_gen.Pulse
            The Pulse object.
        operation_name : str, optional
            The name of the operation corresponding to the pulse.
            If no name is specified, the name of the pulse will be the
            operation name.
        """

        pulse_name = pulse.pulse_name
        pulse_config = pulse.config
        wf_i, wf_q = pulse.waveform

        self.config["pulses"][pulse_name] = pulse_config
        self.config["waveforms"][wf_i.name] = wf_i.config
        self.config["waveforms"][wf_q.name] = wf_q.config

        resonator = self.resonators[resonator_index]

        if not operation_name:
            operation_name = pulse_name

        resonator.add_operation(operation_name, pulse_name)
        self.config["elements"][resonator.name] = resonator.config
        for integ_name, weights in pulse.integ.items():
            self.config["integration_weights"][integ_name] = weights

    def export_json(self, name):
        """
        Export the config as a json file.

        Parameters
        ----------
        name : str
            The name of the file to write into.
        """

        with open(name, "w") as f:
            f.write(json.dumps(self.config))
