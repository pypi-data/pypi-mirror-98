# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     host_windows.py
# Date:     08.Mar.2021
###############################################################################

from __future__ import annotations

from buildnis.modules.config import CmdOutput
from buildnis.modules.helpers.execute import ExeArgs, runCommand


################################################################################
def getCPUInfo() -> CmdOutput:
    """Gets CPU info using `wmic`.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    ret_val = runCommand(
        exe_args=ExeArgs(
            "wmic",
            [
                "cpu",
                "get",
                "L2CacheSize,L3CacheSize,NumberOfLogicalProcessors,NumberOfCores",
            ],
        ),
    )

    return ret_val


################################################################################
def getCPUName() -> CmdOutput:
    """Gets the CPU name using `wmic`

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(exe_args=ExeArgs("wmic", ["cpu", "get", "Name"]))


################################################################################
def getGPUInfo() -> CmdOutput:
    """Returns the GPU names.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(
        exe_args=ExeArgs("wmic", ["path", "win32_VideoController", "get", "name"])
    )


################################################################################
def getMemInfo() -> CmdOutput:
    """Returns the RAM size in bytes.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(exe_args=ExeArgs("wmic", ["memorychip", "get", "capacity"]))
