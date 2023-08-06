# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     project_dependency.py
# Date:     19.Feb.2021
###############################################################################

from __future__ import annotations

import datetime
import os
import pathlib
from typing import List

from buildnis.modules.config import PROJECT_DEP_FILE_NAME, FilePath
from buildnis.modules.config.json_base_class import JSONBaseClass, setAttrIfNotExist
from buildnis.modules.helpers.execute import (
    ExeArgs,
    RunRegex,
    doesExecutableWork,
    runCommand,
)
from buildnis.modules.helpers.files import returnExistingFile
from buildnis.modules.helpers.web import doDownload


class ProjectDependency(JSONBaseClass):
    """Parses the project dependency configuration file and checks the
    dependencies.

    Parses the project dependency JSON file and saves the config file to
    `dependency_cfg`. Checks the dependencies and tries to download and
    install missing dependencies. Writes the altered configuration to the JSON
    file.

    Attributes:
        config_path (FilePath): Path to the project dependency JSON file
        dependencies (List[object]):  The list of dependencies

        Dependency object attributes:

        name (str): the dependency's name
        website_url (str): website to get information about the dependency
        download_url (str): website to download the dependency
        download_dir (str): path to the directory to download the dependency to
        install_cmd (str): command line to call to install the dependency
        install_arguments (List[str]): arguments to pass to the install command
        ok_if_exists (FilePath): if this file exists, the dependency has been
                                 successfully installed
        ok_if_executable (FilePath): if this file is executable, the dependency
                                     has been successfully installed
        executable_argument (str): the argument to call `ok_if_executable` with
                                    to test it
        executable_check_regex (str): the regex to parse the output of
                                      `ok_if_executable` with. If a match is
                                      found,  the dependency has been
                                      successfully installed
        is_checked (bool): if this is true, the dependency has been successfully
                            installed

    Methods:
        checkDependencies: Checks all dependencies in the list of dependencies
                            `dependencies`, if the dependency is installed.
        isDependencyFulfilled: Returns `True`if the dependency has been
                            installed.
        installDep: Installs the given dependency.
        isExecuteableDep: Checks, if the given dependency's executable works,
                        that is, returns the expected string.
    """

    ###########################################################################
    def __init__(self, dependency_config: FilePath, json_path: FilePath) -> None:
        """Parses the project dependency JSON configuration file.

        Args:
            dependency_config (FilePath): the configuration file of project
                                            dependencies to load
            json_path (FilePath): The path to the JSON file to write the result.
        """
        super().__init__(
            config_file_name=PROJECT_DEP_FILE_NAME, config_name="project dependencies"
        )

        self.config_path = os.path.normpath(dependency_config)
        self.json_path = json_path

        read_config_path = returnExistingFile([self.json_path, self.config_path])

        self.readJSON(json_path=read_config_path)

        self.addAttributesIfNotExist({"dependencies", []})

    ############################################################################
    def checkDependencies(self, force_check: bool = False) -> None:
        """Runs all configured dependency checks.

        Checks for each dependency if the configured file exists or the
        configured executable works. If not, it tries to download and/or install
        the dependency and tries again.

        Args:
            force_check (bool, optional): if this is `True`, check the
                        dependency even if it has been checked before - if
                        `is_checked` is `True`. Defaults to False.
        """
        for dep in self.dependencies:

            ProjectDependency.setMustHaveAttribs(dep)

            if dep.is_checked is False or force_check is True:
                self.checkIFInstalled(dep)
            else:
                self._logger.info(
                    'Project dependency "{name}" has already been checked OK'.format(
                        name=dep.name
                    )
                )

        self.generated_at = datetime.datetime.now(tz=None).isoformat(
            sep=" ", timespec="seconds"
        )

    ############################################################################
    def checkIFInstalled(self, dep: object) -> None:
        """Check if the dependency is installed, if not, install it and check again.

        Args:
            dep (object): The dependency object to check.
        """
        if not self.isDependencyFulfilled(dep):
            self.installDep(dep)
            dep.is_checked = self.isDependencyFulfilled(dep)

    ############################################################################
    @staticmethod
    def setMustHaveAttribs(dep: object) -> None:
        """Sets the attributes a dependency object instance must have.

        Args:
            dep (object): The object to check for must-have attributes.
        """
        must_have_attrs = {
            "name": "",
            "website_url": "",
            "download_url": "",
            "download_dir": "",
            "install_cmd": "",
            "ok_if_exists": "",
            "executable_check_regex": "",
            "executable_argument": "",
            "ok_if_executable": "",
            "is_checked": False,
            "install_arguments": [],
        }
        setAttrIfNotExist(instance=dep, attr=must_have_attrs)

    ############################################################################
    def isDependencyFulfilled(self, dep: object) -> bool:
        """Checks if the given dependency is installed.

        Checks if the configured path exist or the configured executable works.

        Args:
            dep (object): the dependency object to check

        Returns:
            bool: `True`, if the dependency has been found
                  `False` else
        """
        self._logger.info(
            'Checking if dependency "{name}" is installed ...'.format(name=dep.name)
        )

        ret_val = False

        if dep.ok_if_exists != "":
            ret_val = self.okIfExists(dep)

        if dep.ok_if_executable != "":
            ret_val = self.okIfExecutable(dep)

        if ret_val is True:
            return ret_val

        self._logger.error('dependency "{name}" not found!'.format(name=dep.name))
        dep.is_checked = False
        return ret_val

    ############################################################################
    def okIfExists(self, dep: object) -> bool:
        """Check if the dependency is installed by checking the existence of a path.

        Args:
            dep (object): The object to check if it is installed.

        Returns:
            bool: `True`, if the path exists, `False` else.
        """
        try:
            if (
                pathlib.Path(dep.ok_if_exists).is_file()
                or pathlib.Path(dep.ok_if_exists).is_dir()
            ):
                self._logger.info(
                    'Path "{path}" exists, dependency "{name}" is installed'.format(
                        path=dep.ok_if_exists, name=dep.name
                    )
                )
                dep.is_checked = True
                return True
            self._logger.error(
                'Path "{path}" does not exist, dependency "{name}" not found!'.format(
                    path=dep.ok_if_exists, name=dep.name
                )
            )
        except Exception as excp:
            self._logger.error('error "{error}"'.format(error=excp))

        return False

    ############################################################################
    def okIfExecutable(self, dep: object) -> bool:
        """Check if the executable of the object is executable, that is, exists and
        generates output.

        Args:
            dep (object): The object to check if it'S configured executable is actually
                            executable.

        Returns:
            bool: `True`, if the configured executable is callable, `False` else.
        """
        self._logger.info(
            'Checking executable "{exe}"'.format(exe=dep.ok_if_executable)
        )
        dep.is_checked = self.isExecuteableDep(dep)
        if dep.is_checked:
            self._logger.info(
                'executable "{exe}" works, dependency "{name}" is installed'.format(
                    exe=dep.ok_if_executable, name=dep.name
                )
            )
            return True

        return False

    ############################################################################
    def installDep(self, dep: object) -> None:
        """Download and/or install the given dependency.

        Args:
            dep (object): the dependency to install or download
        """
        if dep.download_url != "":
            self.download(dep)

        if dep.install_cmd != "":
            self.install(dep)

    ############################################################################
    def install(self, dep: object) -> None:
        """Install the dependency.

        Args:
            dep (object): The dependency object to install.
        """
        try:
            self._logger.info(
                'trying to install "{name}" using command "{cmd}" with args "{args}"'.format(
                    name=dep.name, cmd=dep.install_cmd, args=dep.install_arguments
                )
            )
            output = runCommand(
                exe_args=ExeArgs(dep.install_cmd, dep.install_arguments)
            )
            self._logger.debug(output.std_out)
            self._logger.debug(output.err_out)
        except Exception as excp:
            self._logger.error(
                'error "{error}" trying to install "{name}" using command "{cmd}" with args "{args}"'.format(
                    error=excp,
                    name=dep.name,
                    cmd=dep.install_cmd,
                    args=dep.install_arguments,
                )
            )

    ############################################################################
    def download(self, dep: object) -> None:
        """Download the dependency.

        Args:
            dep (object): The dependency object to download.
        """
        try:
            self._logger.info(
                'Trying to download "{name}" from URL "{url}" to "{path}"'.format(
                    name=dep.name, url=dep.download_url, path=dep.download_dir
                )
            )
            doDownload(url=dep.download_url, to=dep.download_dir)
        except Exception as excp:
            self._logger.error(
                'error "{error}" trying to download "{name}" from URL "{url}" to "{path}"'.format(
                    error=excp,
                    name=dep.name,
                    url=dep.download_url,
                    path=dep.download_dir,
                )
            )

    ############################################################################
    def isExecuteableDep(self, dep: object) -> bool:
        """Execute the dependency, if that works, returns `True`.

        Args:
            dep (object): the dependency to run

        Returns:
            bool: `True` if the executable has been running OK and returns the
                         configured string.
                  `False` else
        """
        self._logger.info(
            'Checking dependency "{name}", try to run executable "{exe}" with argument "{arg}" against regex "{regex}"'.format(
                name=dep.name,
                exe=dep.ok_if_executable,
                arg=dep.executable_argument,
                regex=dep.executable_check_regex,
            )
        )

        try:
            matched_string = doesExecutableWork(
                exe_args=ExeArgs(dep.ok_if_executable, [dep.executable_argument]),
                check_regex=RunRegex(dep.executable_check_regex, 0),
            )

            if matched_string != "":
                return True

        except Exception as excp:
            self._logger.error(
                'error "{error}" dependency "{name}", trying to run executable "{exe}" with argument "{arg}" against regex "{regex}"'.format(
                    error=excp,
                    name=dep.name,
                    exe=dep.ok_if_executable,
                    arg=dep.executable_argument,
                    regex=dep.executable_check_regex,
                )
            )

        return False

    ############################################################################
    def writeJSON(self, json_path: FilePath = "", to_ignore: List[str] = None) -> None:
        """Writes the generated dependency configuration to disk.

        Args:
            json_path (FilePath, optional): The path to the JSON file to write to.
                                        Defaults to "", this uses the saved path.
            to_ignore (List[str]): The list of attributes to ignore.
        """
        if json_path == "":
            super().writeJSON(json_path=self.json_path, to_ignore=to_ignore)
        else:
            super().writeJSON(json_path=json_path, to_ignore=to_ignore)
