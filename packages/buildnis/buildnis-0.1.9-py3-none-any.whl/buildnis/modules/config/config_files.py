# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     config_files.py
# Date:     09.Mar.2021
###############################################################################

from __future__ import annotations

from typing import NamedTuple

from buildnis.modules.config import FilePath


class ConfigTuple(NamedTuple):
    """Class to hold the path of a file and a `bool` that is `True` if the file
    already exists.

    Attributes:
        path (FilePath): The path of the file.
        exists (bool): `True`if the file already exists on disk, `False` otherwise.
    """

    path: FilePath = ""
    exists: bool = False


class ConfigFiles(NamedTuple):
    """Holds the path and state of all JSON configuration files.

    Attributes:
        host_cfg (ConfigTuple): The host configuration, the path to the host
                                configuration JSON file and its status.
        build_tools_Cfg (ConfigTuple): The build tools configuration JSON file path and
                                        its status.
        project_dep_cfg (ConfigTuple): The project dependency configuration JSON file
                                       path and its status.
        project_cfg (ConfigTuple):  THe project configuration JSON file path and its
                                    status.
    """

    host_cfg: ConfigTuple
    build_tools_cfg: ConfigTuple
    project_dep_cfg: ConfigTuple
    project_cfg: ConfigTuple
