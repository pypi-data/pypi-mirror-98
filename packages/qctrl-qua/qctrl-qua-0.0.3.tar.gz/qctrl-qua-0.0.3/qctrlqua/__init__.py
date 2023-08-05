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
The Q-CTRL Python QUA package allows you to integrate BOULDER OPAL with the QUA
quantum computing language.
"""

__author__ = "Q-CTRL <support@q-ctrl.com>"
__version__ = "0.0.3"

from .qua_config_gen import (
    Pulse,
    QmConfig,
    qctrl_pulse_to_samples,
)

__all__ = ["QmConfig", "Pulse", "qctrl_pulse_to_samples"]
