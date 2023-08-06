# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     Config.py
# Date:     13.Feb.2021
###############################################################################

from __future__ import annotations

import os
import pathlib
from typing import List

from buildnis.modules import EXT_ERR_DIR
from buildnis.modules.config import (
    BUILD_CONF_PATH,
    PROJECT_FILE_NAME,
    FilePath,
    config_values,
    project_dependency,
)
from buildnis.modules.config.build_config import BuildCfg
from buildnis.modules.config.check import Check
from buildnis.modules.config.json_base_class import JSONBaseClass
from buildnis.modules.config.module import ModuleCfg
from buildnis.modules.helpers.files import returnExistingFile


class Config(JSONBaseClass):
    """Loads all JSON configurations.

    Parses the project's JSON configuration, all module JSON configurations and
    all build tool JSON configurations.

    Attributes:
    config_path (FilePath): the path to the project's main JSON configuration.
    project_cfg_dir (FilePath): The directory part of `config_path`
    project_cfg (obj): the project's JSON configuration stored in a Python class.
    module_cfgs (Dict[FilePath, Any]) the module JSON configurations
                                      (mentioned in project_cfg)
    build_cfgs (Dict[FilePath, Any]) the build JSON configurations
                                        (mentioned in the module JSONs)
    _logger (logging.Logger): the logger to use

    Methods:
    parseModuleCfgs: Parses the module JSON configurations setup in the project
                    JSON
    parseBuildCfgs: Parses the build JSON configurations setup in the module
                    JSONs
    setHostConfigPath: Sets the path to the generated host config file
    setBuildToolCfgPath: Sets the path to the generated build tool config file
    setProjDepCfgPath: Sets the path to the generated project dependency config file
    getProjCfgDict: Get the project configuration as a JSON sequenceable dict
    """

    ###########################################################################
    def __init__(self, project_config: FilePath, json_path: FilePath) -> None:
        """Constructor of class Config.

        Parses the project's JSON configuration and stores it to project_cfg.

        Arguments:
            project_config (FilePath): the path to the project's JSON configuration
                                        file to read.
            json_path (FilePath): The path to the JSON file to write the result.
        """
        super().__init__(config_file_name=PROJECT_FILE_NAME, config_name="project")

        self.project_dep_cfg: project_dependency.ProjectDependency = None
        self.config_path = project_config
        self.json_path = json_path

        read_config_path = returnExistingFile([self.json_path, self.config_path])

        self.readJSON(json_path=read_config_path)

        self.project_dependency_config = os.path.abspath(
            "/".join(
                [
                    os.path.dirname(self.config_path),
                    os.path.basename(self.project_dependency_config),
                ]
            )
        )

        self.project_cfg_dir = os.path.abspath(os.path.dirname(self.config_path))

        must_have_attrs = [
            "config_path",
            "email",
            "web_url",
            "copyright_info",
            "company",
            "author",
            "version",
            "name",
        ]
        for attr in must_have_attrs:
            if not hasattr(self, attr):
                setattr(self, attr, "")

        self.setProjectConstants()

        # only if not reading from already written configs.
        if read_config_path == self.config_path:
            self.module_cfgs = []

            self.build_cfgs = []

            self.parseModuleCfgs()

            self.parseBuildCfgs()
        else:
            self.readConfigsJSON()

        self.connectModulesBuildTools()

    ############################################################################
    def setProjectConstants(self) -> None:
        """Sets the global project constants to be replaced by placeholders."""
        config_values.PROJECT_CONFIG_DIR_PATH = self.project_cfg_dir
        config_values.PROJECT_NAME = self.name
        config_values.PROJECT_VERSION = self.version
        config_values.PROJECT_AUTHOR = self.author
        config_values.PROJECT_COMPANY = self.company
        config_values.PROJECT_COPYRIGHT_INFO = self.copyright_info
        config_values.PROJECT_WEB_URL = self.web_url
        config_values.PROJECT_EMAIL = self.email
        config_values.PROJECT_ROOT = os.path.abspath(os.path.dirname(self.config_path))

    ############################################################################
    def readConfigsJSON(self) -> None:
        """Reads all module and build configurations from their JSON files."""
        tmp_modules = []
        for module in self.module_cfgs:
            tmp_module = ModuleCfg.fromReadJSON(module)
            tmp_modules.append(tmp_module)
        self.module_cfgs = tmp_modules
        tmp_build_cfgs = []

        self.readBuildCfgs()

        self.build_cfgs = tmp_build_cfgs
        self.reReadIfChangedOnDisk()
        for module in self.module_cfgs:
            module.reReadIfChangedOnDisk()

    ############################################################################
    def readBuildCfgs(self) -> None:
        """Reads the build configs from the generated JSON configuration.
        Rereads them if necessary.
        """
        for module in self.module_cfgs:
            for target in module.targets:
                self.readSingleTarget(target)

    #############################################################################
    @staticmethod
    def readSingleTarget(target: object) -> None:
        """Transforms the deserialized JSON object into a `BuildCfg` object.
        Rereads the original from disk if it has changed.

        Args:
            target (object): The read deserialized build config object.
        """
        if hasattr(target, "build_tool"):
            tmp_bcfg = BuildCfg.fromReadJSON(target.build_tool)
            target.build_tool = tmp_bcfg
            target.build_tool.reReadIfChangedOnDisk()

    ###########################################################################
    def parseModuleCfgs(self) -> None:
        """Parses the module JSON configurations.

        Parses and stores all module JSON configurations configured in the
        project's setup stored in self.project_cfg. Stores the configurations
        in module_cfgs.
        """
        tmp_module_paths = []
        for module in self.modules:

            module_path = os.path.abspath(os.path.join(self.project_cfg_dir, module))

            module_cfg = ModuleCfg(module_config=module_path, json_path="bla")

            tmp_module_paths.append(module_path)

            module_cfg.module_path = os.path.normpath(os.path.dirname(module_path))

            self.module_cfgs.append(module_cfg)

        self.modules = tmp_module_paths

    ###########################################################################
    def parseBuildCfgs(self) -> None:
        """Parses the build JSON configurations.

        Parses all JSON build configurations in `./build_conf`.
        """
        config_dir = pathlib.Path("/".join([self.project_cfg_dir, BUILD_CONF_PATH]))
        if not config_dir.is_dir():
            self._logger.critical(
                'error loading build configurations, "{path}" does not exist or is not a directory!'.format(
                    path=config_dir
                )
            )
            os.system.exit(EXT_ERR_DIR)

        self.build_cfgs = []
        for config_file in config_dir.glob("*.json"):
            try:
                tmp_cfg = BuildCfg(
                    build_config=str(config_file.absolute()), json_path="bla"
                )
                self.build_cfgs.append(tmp_cfg)
            except Exception as excp:
                self._logger.error(
                    'error "{error}" loading build configuration "{path}"'.format(
                        error=excp, path=config_file
                    )
                )

        # TODO OS dir configs!

    ############################################################################
    def connectModulesBuildTools(self) -> None:
        """For each target in each module: search for the build tool and put it
        into this module's target.
        """
        for module in self.module_cfgs:
            for target in module.targets:
                self.connectInTarget(target)

    ############################################################################
    def connectInTarget(self, target: object) -> None:
        """Connects the build configuration with the given target.

        Args:
            target (object): The target to search the build config for and connect it.
        """
        build_type = target.build_type
        build_subtype = target.build_subtype
        build_tool_type = target.build_tool_type
        for build_cfg in self.build_cfgs:
            if (
                build_cfg.build_type == build_type
                and build_cfg.build_subtype == build_subtype
                and build_cfg.build_tool_type == build_tool_type
            ):
                target.build_tool = build_cfg

    ############################################################################
    def writeJSON(self, json_path: FilePath = "", to_ignore=None) -> None:
        """Writes the project's config to a JSON file.

        Args:
            json_path (FilePath, optional): The path to the JSON file to write to.
                                        Defaults to "", this uses the saved path.
            to_ignore (list, optional): List of attributes to ignore, to not save to
                                        disk. Defaults to ["project_dep_cfg"].
        """
        if to_ignore is None:
            to_ignore = ["project_dep_cfg", "build_cfgs"]
        if json_path == "":
            super().writeJSON(json_path=self.json_path, to_ignore=to_ignore)
        else:
            super().writeJSON(json_path=json_path, to_ignore=to_ignore)

    ###########################################################################
    def setHostConfigPath(self, path: FilePath) -> None:
        """Sets the path to the generated host config JSON file.

        Args:
            path (FilePath): the path to the host config file
        """
        self.host_cfg_file = os.path.abspath(path)

    ###########################################################################
    def setBuildToolCfgPath(self, path: FilePath) -> None:
        """Sets the path to the generated build tools config JSON file.

        Args:
            path (FilePath): the path to the build tools config file
        """
        self.build_tools_cfg_file = os.path.abspath(path)

    ###########################################################################
    def setProjDepCfgPath(self, path: FilePath) -> None:
        """Sets the path to the generated project dependency config JSON file.

        Args:
            path (FilePath): the path to the project dependency config file.
        """
        self.project_dependency_config_file = os.path.abspath(path)

    ###########################################################################
    def expandAllPlaceholders(self, parents: List[object] = None) -> None:
        """Goes through all configurations and replaces placeholders in their
        elements. A Placeholder is a string like `${PLACEHOLDER}`, a dollar
        sign followed by a curly opening brace, the string to replace and the
        closing curly brace.

        Args:
            parents (List[object], optional): The list of parent objects.
                                            Defaults to None.
        """
        if self.project_dep_cfg is not None:
            self.project_dep_cfg.reReadIfChangedOnDisk()
        super().expandAllPlaceholders(parents=parents)

    ###########################################################################
    def checkDependencies(self, force_check: bool = False) -> None:
        """Calls the `checkDependencies` method of the project dependency
        configuration.

        Args:
            force_check (bool, optional): if this is `True`, check the
                        dependency even if it has been checked before - if
                        `is_checked` is `True`. Defaults to False.
        """
        if self.project_dep_cfg is not None:
            self.project_dep_cfg.checkDependencies(force_check)

    ############################################################################
    def searchBuildTools(self, build_tool_cfg: Check) -> None:
        """Searches for a build tool in all found build tools.
        Connects it with a build configuration.

        Args:
            build_tool_cfg (Check): The build tools config to search for build tools.
        """
        for build_cfg in self.build_cfgs:
            for stage in build_cfg.stages:
                self.searchInStage(build_tool_cfg, stage)

    ############################################################################
    def searchInStage(self, build_tool_cfg: Check, stage: object) -> None:
        """Searches for a build tool configured in a stage of a build configuration.

        Args:
            build_tool_cfg (Check): The build tool configuration to search in.
            stage (object): The stage containing the build tool name to search for.
        """
        if hasattr(stage, "build_tool"):
            self._logger.debug(
                "Build config stage already has a build tool, not doing anything"
            )
            return
        search_name = stage.build_tool_name
        self._logger.info(
            'build config: searching for buildtool "{name}"'.format(name=search_name)
        )
        build_tool = build_tool_cfg.searchBuildTool(name=search_name)
        if build_tool is not None:
            stage.build_tool = build_tool
