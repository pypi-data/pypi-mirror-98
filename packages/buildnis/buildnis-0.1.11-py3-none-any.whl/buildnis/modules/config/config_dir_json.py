# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     config_dir_json.py
# Date:     02.Mar.2021
###############################################################################

from __future__ import annotations

import os
import sys
from typing import List

from buildnis.modules import EXT_ERR_DIR
from buildnis.modules.config import CFG_DIR_NAME, FilePath
from buildnis.modules.config.json_base_class import JSONBaseClass
from buildnis.modules.helpers.files import checkIfIsFile, makeDirIfNotExists


class ConfigDirJson(JSONBaseClass):
    """Class to handle the configuration of the directory all generated
    configuration files are written to.

    Attributes:
        file_name (FilePath):  The path to the JSON configuration file
        cfg_path (FilePath): The directory to save generated configurations to

    Methods:
        writeJSON: Writes the configuration directory configuration to a JSON
                    file with path `file_name`.
    """

    ############################################################################
    def __init__(
        self, file_name: FilePath, working_dir: FilePath, cfg_path: FilePath = ""
    ) -> None:
        """Loads an existing configuration directory configuration if it exists,
        or uses the given path from the command line argument `--generate-conf-dir`.

        Args:
            file_name (FilePath): The file name of the configuration directory
                                    configuration, should be something like
                                    `working_dir/CFG_DIR_NAME`
            working_dir (FilePath): path of the working directory, the directory the
                                    project config is located in (needed to find an
                                    existing configuration directory configuration file)
            cfg_path (FilePath, optional): The path to the configuration directory.
                                            Defaults to "".
        """
        super().__init__(
            config_file_name=CFG_DIR_NAME, config_name="configuration directory"
        )

        self.json_path = file_name

        if cfg_path != "":
            if os.path.isabs(cfg_path):
                self.cfg_path = os.path.normpath(cfg_path)
            else:
                self.cfg_path = os.path.abspath("/".join([working_dir, cfg_path]))
        else:
            try:
                if checkIfIsFile(file_name) is False:
                    self.cfg_path = os.path.abspath(working_dir)
                else:
                    self.readJSON(json_path=file_name)
                    self.cfg_path = os.path.abspath(self.cfg_path)
            except Exception as excp:
                self._logger.critical(
                    'error "{error}" loading configuration directory configuration "{path}"'.format(
                        error=excp, path=file_name
                    )
                )
                sys.exit(EXT_ERR_DIR)

        try:
            makeDirIfNotExists(self.cfg_path)
        except Exception as excp:
            self._logger.critical(
                'error "{error}" trying to generate directory "{path}"'.format(
                    error=excp, path=cfg_path
                )
            )
            sys.exit(EXT_ERR_DIR)

    ############################################################################
    def writeJSON(self, json_path: FilePath = "", to_ignore: List[str] = None) -> None:
        """Writes the path to the project config directory to a JSON file with
        the given path `json_path`.

        Args:
            json_path (str, optional): The path to the JSON file to write to.
                                        Defaults to "", this uses the saved path.
             to_ignore (List[str]): The list of attributes to ignore
        """
        try:
            if json_path == "":
                super().writeJSON(json_path=self.json_path, to_ignore=to_ignore)
            else:
                super().writeJSON(json_path=json_path, to_ignore=to_ignore)

        except Exception as excp:
            self._logger.critical(
                'error "{error}" trying to write configuration directory configuration "{path}"'.format(
                    error=excp, path=self.file_name
                )
            )
