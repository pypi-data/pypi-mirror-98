# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     host_linux.py
# Date:     08.Mar.2021
###############################################################################

from __future__ import annotations

from buildnis.modules.config import CmdOutput
from buildnis.modules.helpers.execute import ExeArgs, runCommand


################################################################################
def getOSMajVers() -> CmdOutput:
    """Returns the major OS version.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(
        exe_args=ExeArgs(
            "bash",
            [
                "-c",
                "grep NAME /etc/os-release |head -1|cut -d'=' -f2|tr -d '\"'",
            ],
        )
    )


################################################################################
def getOSVer() -> CmdOutput:
    """Returns the minor OS version.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(
        exe_args=ExeArgs(
            "bash",
            [
                "-c",
                "grep VERSION /etc/os-release |head -1|cut -d'=' -f2|tr -d '\"'",
            ],
        )
    )


################################################################################
def getCPUNameLinux() -> CmdOutput:
    """Returns the CPU's name.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(
        exe_args=ExeArgs(
            "bash",
            ["-c", "grep 'model name' /proc/cpuinfo |head -1|cut -d':' -f2-"],
        )
    )


################################################################################
def getNumCoresLinux() -> CmdOutput:
    """Returns the number of physical cores.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(
        exe_args=ExeArgs(
            "bash",
            ["-c", "grep 'cpu cores' /proc/cpuinfo |uniq|cut -d':' -f2"],
        )
    )


################################################################################
def getNumLogCoresLinux() -> CmdOutput:
    """Returns the number of logical cores, including the hyperthreading.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(
        exe_args=ExeArgs(
            "bash",
            ["-c", "grep siblings /proc/cpuinfo |uniq |cut -d':' -f2"],
        )
    )


################################################################################
def getL2CacheLinux() -> CmdOutput:
    """Returns the size of the CPU's level 2 cache.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(
        exe_args=ExeArgs(
            "bash",
            ["-c", "getconf -a|grep LEVEL2_CACHE_SIZE|awk '{print $2}'"],
        )
    )


################################################################################
def getL3CacheLinux() -> CmdOutput:
    """Returns the size of the CPU's level 3 cache.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(
        exe_args=ExeArgs(
            "bash",
            ["-c", "getconf -a|grep LEVEL3_CACHE_SIZE|awk '{print $2}'"],
        )
    )


################################################################################
def getRAMSizeLinux() -> CmdOutput:
    """Returns the RAM size in bytes.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(
        exe_args=ExeArgs("bash", ["-c", "free -b|grep 'Mem:'|awk '{print $2}'"])
    )


################################################################################
def getGPUNamesLinux() -> CmdOutput:
    """Returns the names of the GPUs.

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(exe_args=ExeArgs("bash", ["-c", "lspci|grep VGA|cut -f3 -d':'"]))


################################################################################
def getGPUNamesSbinLinux() -> CmdOutput:
    """Returns the names of the GPUs, using `/sbin/lspci` because some distributions
    don't have `lspci` in `/usr/bin`

    Returns:
        CmdOutput: The output of the command, as a `CmdOutput` instance containing
                    `stdout` and `stderr` as attributes.
    """
    return runCommand(
        exe_args=ExeArgs("bash", ["-c", "/sbin/lspci|grep VGA|cut -f3 -d':'"])
    )
