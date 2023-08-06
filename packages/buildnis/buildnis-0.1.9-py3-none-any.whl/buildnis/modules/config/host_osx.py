# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     host_osx.py
# Date:     08.Mar.2021
###############################################################################

from __future__ import annotations

from buildnis.modules.config import CmdOutput
from buildnis.modules.helpers.execute import ExeArgs, runCommand


################################################################################
def getOSName() -> CmdOutput:
    """Returns the OS version of OS X.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(exe_args=ExeArgs("sw_vers", ["-productVersion"]))


################################################################################
def getCPUNameOSX() -> CmdOutput:
    """Returns the CPU name.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(exe_args=ExeArgs("sysctl", ["-n", "machdep.cpu.brand_string"]))


################################################################################
def getNumCoresOSX() -> CmdOutput:
    """Returns the number of physical cores.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(exe_args=ExeArgs("sysctl", ["-n", "hw.physicalcpu"]))


################################################################################
def getNumLogCoresOSX() -> CmdOutput:
    """Returns the number of logical cores, including hyperthreading.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(exe_args=ExeArgs("sysctl", ["-n", "hw.logicalcpu"]))


################################################################################
def getL2CacheOSX() -> CmdOutput:
    """Returns the size of the CPU's level 2 cache.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(exe_args=ExeArgs("sysctl", ["-n", "hw.l2cachesize"]))


################################################################################
def getL3CacheOSX() -> CmdOutput:
    """Returns the size of the CPU's level 3 cache.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(exe_args=ExeArgs("sysctl", ["-n", "hw.l3cachesize"]))


################################################################################
def getRAMSizeOSX() -> CmdOutput:
    """Returns the RAM size in bytes.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(exe_args=ExeArgs("sysctl", ["-n", "hw.memsize"]))


################################################################################
def getGPUOSX() -> CmdOutput:
    """Return the GPU names.

    Returns:
         CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(exe_args=ExeArgs("system_profiler", ["SPDisplaysDataType"]))
