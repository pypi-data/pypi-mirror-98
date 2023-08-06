# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     host.py
# Date:     15.Feb.2021
###############################################################################

from __future__ import annotations

import platform

from buildnis.modules.config import (
    AMD64_ARCH_STRING,
    CFG_VERSION,
    HOST_FILE_NAME,
    LINUX_OS_STRING,
    OSX_NAME_DICT,
    OSX_OS_STRING,
    WINDOWS_OS_STRING,
    config_values,
)
from buildnis.modules.config.host_linux import (
    getCPUNameLinux,
    getGPUNamesLinux,
    getGPUNamesSbinLinux,
    getL2CacheLinux,
    getL3CacheLinux,
    getNumCoresLinux,
    getNumLogCoresLinux,
    getOSMajVers,
    getOSVer,
    getRAMSizeLinux,
)
from buildnis.modules.config.host_osx import (
    getCPUNameOSX,
    getGPUOSX,
    getL2CacheOSX,
    getL3CacheOSX,
    getNumCoresOSX,
    getNumLogCoresOSX,
    getOSName,
    getRAMSizeOSX,
)
from buildnis.modules.config.host_windows import (
    getCPUInfo,
    getCPUName,
    getGPUInfo,
    getMemInfo,
)
from buildnis.modules.config.json_base_class import JSONBaseClass
from buildnis.modules.helpers.files import checkIfExists


class Host(JSONBaseClass):
    """Holds all information about the host this is running on.

    Stores hostname, OS, OS version, CPU architecture, RAM, CPU name, ...

    Attributes
        host_name (str):      This host's name
        os (str):             The OS this is running on (like "Windows", "Linux")
        os_vers_major (str):  Major version of the OS (like "10" for Windows 10)
        os_vers (str):        Excact version string
        cpu_arch (str):       CPU architecture, like "x64" or "x86"
        cpu (str):            The detailed name of the CPU
        file_name (str):      The JSON identifier of the host config file, part
                              of the file name
        level2_cache (int):   Size of the CPU's level 2 cache, in bytes
        level3_cache (int):   Size of the CPU's level 3 cache, in bytes
        num_cores (int):      The number of physical cores
        num_logical_cores (int): The number of logical, 'virtual' cores
        ram_total (int):      Amount of physical RAM in bytes
        gpu List[str]:        The list of names of all GPUs
        python_version (str): The version of this host's Python interpreter
        json_path(str):       The path to the written JSON host config file

    Methods
        collectWindowsConfig: adds information, that has to be collected in a
                            Windows specific way
        collectLinuxConfig: adds information, that has to be collected in a
                            Linux specific way
        collectOSXConfig:   adds information, that has to be collected in a
                            Mac OS X specific way
    """

    ###########################################################################
    def __init__(self) -> None:
        """Constructor of class Host, gathers and sets the host's environment.

        Like OS, hostname, OS version, CPU architecture, ...
        """
        super().__init__(config_file_name=HOST_FILE_NAME, config_name="host")

        self._logger.info("Gathering information about this host ...")

        self.file_name = HOST_FILE_NAME
        self.file_version = ".".join(CFG_VERSION)

        self.getOSInfo()

        self.python_version = platform.python_version()

        if self.os == WINDOWS_OS_STRING:
            self.collectWindowsConfig()

        elif self.os == LINUX_OS_STRING:
            self.collectLinuxConfig()

        elif self.os == OSX_OS_STRING:
            self.collectOSXConfig()

        else:
            self._logger.error(
                'error, "{os_name}" is a unknown OS!'.format(os_name=self.os)
            )
            self._logger.error(
                'You can add support of this OS to the file "modules/config/host.py"'
            )
            self._logger.error("")

        self.setConstants()

    ############################################################################
    def setConstants(self) -> None:
        """Set the host constants to use for configuration files."""
        must_have_attrs = {
            "os": "",
            "cpu_arch": "",
            "host_name": "",
            "num_cores": 1,
            "num_logical_cores": 1,
        }
        for attr in must_have_attrs:
            if not hasattr(self, attr):
                setattr(self, attr, must_have_attrs[attr])

        config_values.HOST_OS = self.os
        config_values.HOST_CPU_ARCH = self.cpu_arch
        config_values.HOST_NAME = self.host_name
        config_values.HOST_NUM_CORES = self.num_cores
        config_values.HOST_NUM_LOG_CORES = self.num_logical_cores

    ############################################################################
    def getOSInfo(self) -> None:
        """Gets Info about the OS, like Name, CPU architecture, and similar."""
        (
            self.os,
            self.host_name,
            self.os_vers_major,
            self.os_vers,
            self.cpu_arch,
            self.cpu,
        ) = platform.uname()

        if self.os == "Darwin":
            self.os = OSX_OS_STRING

        if self.cpu_arch in ("AMD64", "x86_64"):
            self.cpu_arch = AMD64_ARCH_STRING

    #############################################################################
    def collectWindowsConfig(self) -> None:
        """Collect information about the hardware we're running on on Windows.

        Calls these commands and parses their outputs:

        wmic cpu get L2CacheSize,L3CacheSize,NumberOfLogicalProcessors,
                                                                    NumberOfCores,Name
        wmic memorychip get capacity
        wmic path win32_VideoController get name
        """
        try:
            self.GetCPUInfo()

            self.collectWinCpuGpuRam()

        except Exception as excp:
            self._logger.error('error "{error}" calling wmic'.format(error=excp))

    ############################################################################
    def GetCPUInfo(self) -> None:
        """Gets the CPU info, like cache sizes, number of cores."""
        cpu_info_cmd = getCPUInfo()
        for line in cpu_info_cmd.std_out.strip().split("\n"):
            self.parseCPUInfoLine(line)

    ############################################################################
    def parseCPUInfoLine(self, line: str) -> None:
        """Parses the output of the CPU info wmic command.

        Args:
            line (str): The line of output to parse.
        """
        try:
            if line != "" and "L2CacheSize" not in line:
                (
                    level2_cache,
                    level3_cache,
                    num_cores,
                    num_logical_cores,
                ) = line.split()
                self.level2_cache = int(level2_cache)
                self.level3_cache = int(level3_cache)
                self.num_cores = int(num_cores)
                self.num_logical_cores = int(num_logical_cores)
        except Exception:
            self.retryCPUInfo(line)

    ############################################################################
    def retryCPUInfo(self, line: str) -> None:
        """Retry getting the CPU info, this time ignore L2Cache (GitHub Windows
        runners doesn't display L2 cache).

        Args:
            line (str): The line of output to parse.
        """
        try:
            if line != "" and "L2CacheSize" not in line:
                (
                    level3_cache,
                    num_cores,
                    num_logical_cores,
                ) = line.split()
                self.level2_cache = 0
                self.level3_cache = int(level3_cache)
                self.num_cores = int(num_cores)
                self.num_logical_cores = int(num_logical_cores)
        except Exception as excp:
            self._logger.error('error "{error}" getting CPU info'.format(error=excp))

    ############################################################################
    def collectWinCpuGpuRam(self):
        """Collects the Windows CPU, GPU and RAM size information."""
        self.getCPU()

        self.getGPU()

        self.getRAM()

    ############################################################################
    def getRAM(self) -> None:
        """Sets the RAM size."""
        mem_info_cmd = getMemInfo()
        self.ram_total = 0
        for line in mem_info_cmd.std_out.strip().split("\n"):
            self.parseRAMline(line)

    ############################################################################
    def parseRAMline(self, line: str) -> None:
        """Parses a single line of output to get the RAM size.

        Args:
            line (str): The line of output to parse.
        """
        if line != "" and "Capacity" not in line:
            try:
                self.ram_total += int(line)
            except Exception as excp:
                self._logger.error(
                    'error "{error}" getting RAM size'.format(error=excp)
                )

    ############################################################################
    def getGPU(self) -> None:
        """Sets the GPU name list."""
        gpu_info_cmd = getGPUInfo()
        self.gpu = []
        for line in gpu_info_cmd.std_out.strip().split("\n"):
            if line != "" and "Name" not in line:
                self.gpu.append(line.strip())

    ############################################################################
    def getCPU(self) -> None:
        """Sets the CPU name."""
        cpu_name_cmd = getCPUName()
        for line in cpu_name_cmd.std_out.strip().split("\n"):
            if line != "" and "Name" not in line:
                self.cpu = line

    #############################################################################
    def collectLinuxConfig(self) -> None:
        """Collect information about the hardware we're running on on Linux.

        Calls the following commands:

        cat /etc/os-release
        NAME="Red Hat Enterprise Linux"
        VERSION="8.3 (Ootpa)"

        grep "model name" /proc/cpuinfo |uniq|cut -d':' -f2
        getconf -a|grep LEVEL2_CACHE_SIZE|awk '{print $2}'
        getconf -a|grep LEVEL3_CACHE_SIZE|awk '{print $2}'
        grep "cpu cores" /proc/cpuinfo |uniq|cut -d':' -f2
        grep "siblings" /proc/cpuinfo |uniq |cut -d':' -f2
        free -b|grep "Mem:"|awk '{print $2}'
        grep "DISTRIB_DESCRIPTION" /etc/lsb-release
        lspci|grep VGA|cut -f3 -d':'
        """
        try:
            try:
                if checkIfExists("/etc/os-release") is True:
                    os_vers_maj = getOSMajVers()
                    self.os_vers_major = os_vers_maj.std_out.strip()

                    os_vers = getOSVer()
                    self.os_vers = os_vers.std_out.strip()
            except Exception as excp:
                self._logger.error(
                    'error "{error}" trying to read /etc/os-release'.format(error=excp)
                )

            self.collectLinuxCpuGpuRam()

        except Exception as excp:
            self._logger.error(
                'error "{error}" getting Linux host information'.format(error=excp)
            )

    ############################################################################
    def collectLinuxCpuGpuRam(self):
        """Collects information about this host's CPU, GPU, and so on on Linux."""
        cpu_name_cmd = getCPUNameLinux()
        self.cpu = cpu_name_cmd.std_out.strip()

        cpu_num_cores = getNumCoresLinux()
        self.num_cores = int(cpu_num_cores.std_out.strip())

        cpu_num_log_cpus = getNumLogCoresLinux()
        self.num_logical_cores = int(cpu_num_log_cpus.std_out.strip())

        cpu_l2_cache = getL2CacheLinux()
        self.level2_cache = int(cpu_l2_cache.std_out.strip())

        cpu_l3_cache = getL3CacheLinux()
        self.level3_cache = int(cpu_l3_cache.std_out.strip())

        ram_size = getRAMSizeLinux()
        self.ram_total = int(ram_size.std_out.strip())
        self.gpu = []

        self.getGPUNamesLinux()

    ############################################################################
    def getGPUNamesLinux(self) -> None:
        """Gets the list of GPU names."""
        self.getGPULspci()

        # some distries (Suse) use /sbin/lspci
        if self.gpu == []:
            self.getGPUSbinLspci()

    ############################################################################
    def getGPUSbinLspci(self) -> None:
        """Gets the GPU names using `lspci`."""
        gpu_info_cmd = getGPUNamesSbinLinux()
        for line in gpu_info_cmd.std_out.strip().split("\n"):
            if line != "":
                self.gpu.append(line.strip())

    ############################################################################
    def getGPULspci(self) -> None:
        """Gets the GPU names using `/sbin/lspci`."""
        gpu_info_cmd = getGPUNamesLinux()
        for line in gpu_info_cmd.std_out.strip().split("\n"):
            if line != "":
                self.gpu.append(line.strip())

    #############################################################################
    def collectOSXConfig(self) -> None:
        """Collect information about the hardware we're running on on MacOS X.

        Using this commands:
        sysctl -n hw.memsize
        sysctl -n hw.physicalcpu
        sysctl -n hw.logicalcpu
        sysctl -n hw.l2cachesize
        sysctl -n hw.l3cachesize
        sysctl -n machdep.cpu.brand_string
        sw_vers -productVersion

        TODO get GPU info: system_profiler SPDisplaysDataType
        """
        try:
            os_name = getOSName()
            self.os_vers = os_name.std_out.strip()

            os_vers_2_digits_list = self.os_vers.rsplit(".")
            self.os_vers_major = OSX_NAME_DICT[".".join(os_vers_2_digits_list[:-1])]

            cpu_name_cmd = getCPUNameOSX()
            self.cpu = cpu_name_cmd.std_out.strip()

            cpu_num_cores = getNumCoresOSX()
            self.num_cores = int(cpu_num_cores.std_out)

            cpu_num_log_cpus = getNumLogCoresOSX()
            self.num_logical_cores = int(cpu_num_log_cpus.std_out)

            cpu_l2_cache = getL2CacheOSX()
            self.level2_cache = int(cpu_l2_cache.std_out)

            cpu_l3_cache = getL3CacheOSX()
            self.level3_cache = int(cpu_l3_cache.std_out)

            ram_size = getRAMSizeOSX()
            self.ram_total = int(ram_size.std_out)

            self.gpu = []
            gpu_out = getGPUOSX()
            self._logger.debug(
                "OSX GPU OUT: {out} {err}".format(
                    out=gpu_out.std_out, err=gpu_out.err_out
                )
            )

        except Exception as excp:
            self._logger.error(
                'error "{error}" gathering information on OS X'.format(error=excp)
            )


################################################################################
def printHostInfo() -> None:
    """To test the collection of the host's information, print all to stdout."""
    print(Host())


################################################################################
if __name__ == "__main__":
    printHostInfo()
