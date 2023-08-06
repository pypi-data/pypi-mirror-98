# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     __init__.py
# Date:     13.Feb.2021
###############################################################################

from __future__ import annotations

import os
from typing import NamedTuple

__all__ = [
    "config",
    "helpers",
    "main",
    "BuildnisException",
    "ProgramVersion",
    "VersionString",
    "MODULE_DIR_PATH",
    "VERSION",
    "EXT_OK",
    "EXT_ERR_LD_FILE",
    "EXT_ERR_CMDLINE",
    "EXT_ERR_DIR",
    "EXT_ERR_WR_FILE",
    "EXT_ERR_PYTH_VERS",
    "EXT_ERR_IMP_MOD",
    "EXT_ERR_NOT_VLD",
]


class BuildnisException(Exception):
    """Base class of all custom exceptions used in this program."""


VersionString = str


class ProgramVersion(NamedTuple):
    """Class to hold the program's version."""

    major: int = 0
    minor: int = 0
    patch: int = 0

    def __str__(self) -> VersionString:
        """Returns the program's version as a string.

        Returns:
            [VersionString]: the programs version as a string `{major}.{minor}.{patch}`
        """
        return "{major}.{minor}.{patch}".format(
            major=self.major, minor=self.minor, patch=self.patch
        )


VERSION = ProgramVersion(major=0, minor=1, patch=9)

MODULE_DIR_PATH = os.path.abspath(os.path.dirname(__file__) + "/../")

# Exit constants, constants passed to ´sys.exit´
EXT_OK = 0
"""No error"""

EXT_ERR_LD_FILE = 1
"""Error reading file"""

EXT_ERR_CMDLINE = 2
"""Error parsing command line"""

EXT_ERR_DIR = 3
"""Error, directory does not exist or is not a directory"""

EXT_ERR_WR_FILE = 4
"""Error writing to file"""

EXT_ERR_PYTH_VERS = 5
"""Error, Python version too old"""

EXT_ERR_IMP_MOD = 6
"""Error importing module"""

EXT_ERR_NOT_VLD = 7
"""Error, file is not a valid configuration"""
