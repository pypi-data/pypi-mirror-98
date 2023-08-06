# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     module.py
# Date:     04.Mar.2021
###############################################################################

from __future__ import annotations

from typing import List

from buildnis.modules.config import MODULE_FILE_NAME, FilePath
from buildnis.modules.config.json_base_class import JSONBaseClass
from buildnis.modules.helpers.file_compare import FileCompare
from buildnis.modules.helpers.files import returnExistingFile


class ModuleCfg(JSONBaseClass):
    """Holds a single module configuration read from a JSON module
    configuration file.

    Methods:
        fromReadJSON: Converts the `SimpleNamespace` instance read from a JSON
                        file  to a ModuleCfg instance to use.
        writeJSON: Writes the configuration to file (not used, because it is
                    part of the project configuration JSON file).
    """

    ###########################################################################
    def __init__(
        self, module_config: FilePath, json_path: FilePath, load_json: bool = True
    ):
        """Loads the file from one of the given JSON paths.

        If `json_path` exists, it is loaded from this file, else `module_config`
        is read.

        Args:
            module_config (FilePath): The path to the original JSON module
                            configuration  file.
            json_path (FilePath): The path where the parsed module configuration
                                    should be saved to. It is not used, because
                                    the `ModuleCFG` instances are part of the
                                    project configuration file.
            load_json (bool, optional): Should the configuration be read from the
                                    file `module_config`. Defaults to True.
        """
        super().__init__(config_file_name=MODULE_FILE_NAME, config_name="module")

        self.config_path = module_config
        self.json_path = json_path

        if load_json:
            read_config_path = returnExistingFile([self.json_path, self.config_path])

            self.readJSON(json_path=read_config_path)

            must_have_attrs = {"name": "", "targets": []}
            for attr in must_have_attrs:
                if not hasattr(self, attr):
                    setattr(self, attr, must_have_attrs[attr])

    ##############################################################################
    @classmethod
    def fromReadJSON(cls, instance: object) -> ModuleCfg:
        """Converts a `SimpleNamespace` instance load from a JSON module
        configuration file to a ModuleCfg instance to use.

        Args:
            instance (object): The `Simplenamespace` instance to convert.

        Returns:
            ModuleCfg: The data of the given object as a `ModuleCfg` instance.
        """
        ret_val = cls(
            module_config=instance.config_path,
            json_path=instance.json_path,
            load_json=False,
        )

        for item in instance.__dict__:
            setattr(ret_val, item, instance.__dict__[item])

        ret_val.orig_file = FileCompare(ret_val.orig_file.path)
        ret_val.orig_file.size = instance.orig_file.size
        ret_val.orig_file.hash = instance.orig_file.hash

        return ret_val

    ##############################################################################
    def writeJSON(self, json_path: FilePath = "", to_ignore: List[str] = None) -> None:
        """Writes the generated config to disk.

        Not used, because it is part of the project configuration file.

        Args:
            json_path (FilePath, optional): The path to the JSON file to write to.
                                        Defaults to "", this uses the saved path.
            to_ignore (List[str]): The list of attributes to ignore.
        """
        if json_path == "":
            super().writeJSON(json_path=self.json_path, to_ignore=to_ignore)
        else:
            super().writeJSON(json_path=json_path, to_ignore=to_ignore)
