# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     json.py
# Date:     21.Feb.2021
###############################################################################

from __future__ import annotations

import datetime
import io
import json
import logging
import os
import sys
from logging import Logger
from types import SimpleNamespace
from typing import Dict, List

from buildnis.modules import EXT_ERR_LD_FILE, EXT_ERR_NOT_VLD, EXT_ERR_WR_FILE
from buildnis.modules.config import CFG_VERSION, FilePath
from buildnis.modules.helpers import LOGGER_NAME
from buildnis.modules.helpers.file_compare import FileCompare

_logger = logging.getLogger(LOGGER_NAME)


################################################################################
def getJSONDict(src: object, to_ignore: List[str] = None) -> Dict:
    """Returns a dictionary suitable to pass to `json.dump(s)`.

    Attention: only works with simple classes obtained from `json.load(s)`.

    Args:
        src (object): The class to serialize.
        to_ignore (List[str]): The list of attribute names to ignore.

    Returns:
        Dict: The dictionary suitable to pass to `json.dump(s)`.
    """
    if to_ignore is None:
        to_ignore = []
    ret_val = {}

    for item in src.__dict__:
        parseItem(src, to_ignore, ret_val, item)

    return ret_val


################################################################################
def parseItem(
    src: object, to_ignore: List[str], ret_val: Dict[str, object], item: object
) -> None:
    """Parses an item of `src`'s dictionary of attributes.

    Args:
        src (object): The object to serialize.
        to_ignore (List[str]): The list of attributes to ignore and not serialize.
        ret_val (Dict[str, object]): The dictionary to return, the serialized object
                                    src.
        item (object): The current item to serialize.
    """
    if item in to_ignore:
        return
    if isinstance(src.__dict__[item], Logger):
        return

    if isinstance(src.__dict__[item], list):
        parseList(src, ret_val, item)
    elif isinstance(src.__dict__[item], FileCompare):
        setFileCompare(src, ret_val, item)
    elif hasattr(src.__dict__[item], "__dict__"):
        ret_val[item] = getJSONDict(src.__dict__[item], to_ignore=to_ignore)
    else:
        ret_val[item] = src.__dict__[item]


################################################################################
def parseList(src, ret_val, item) -> None:
    """Parse the elements of a list.

    Args:
        src (object): The object to serialize.
        ret_val (Dict[str, object]): The dictionary to return, the serialized object
                                    src.
        item (object): The current item to serialize.
    """
    sub_list = []
    for subitem in src.__dict__[item]:
        if hasattr(subitem, "__dict__"):
            sub_list.append(getJSONDict(subitem))
        else:
            sub_list.append(subitem)
    ret_val[item] = sub_list


################################################################################
def setFileCompare(src: object, ret_val: Dict[str, object], item: object) -> None:
    """Set the attributes of the `FileCompare` instance in the JSON dictionary.

    Args:
        src (object): The object to serialize.
        ret_val (Dict[str, object]): The dictionary to return, the serialized object
                                    src.
        item (object): The current item to serialize.
    """
    tmp_dict = {}
    tmp_dict["path"] = src.__dict__[item].__dict__["path"]
    tmp_dict["size"] = src.__dict__[item].__dict__["size"]
    tmp_dict["hash"] = src.__dict__[item].__dict__["hash"]
    ret_val[item] = tmp_dict


################################################################################
def writeJSON(
    json_dict: Dict, json_path: FilePath, file_text: str = "", conf_file_name: str = ""
) -> None:
    """Writes the information contained in the dictionary `json_dict` as JSON.

    If an error occurs, the program is exited with an error message!

    Args:
        json_dict (Dict): The JSON serializeable dict to generate the JSON of
        json_path (FilePath): Path to the JSON file to write
        file_text (str, optional): The name of the JSON configuration file for
                    logging proposes. Defaults to "", which will be logged as
                    'a', like in "Writing _a_ JSON configuration file ...".
        conf_file_name (str, optional): The string that has to be the value of
                    `file_name` in the JSON file, if not, the program exits.
                    Defaults to "".
    """
    if conf_file_name != "":
        json_dict["file_name"] = conf_file_name

    json_dict["file_version"] = ".".join(CFG_VERSION)

    json_dict["json_path"] = os.path.abspath(json_path)

    json_dict["generated_at"] = datetime.datetime.now(tz=None).isoformat(
        sep=" ", timespec="seconds"
    )

    tmp_text = file_text
    if tmp_text == "":
        tmp_text = "a"

    _logger.warning(
        'Writing {text} JSON configuration file "{file}"'.format(
            text=tmp_text, file=json_path
        )
    )

    with io.open(
        json_path,
        mode="w",
    ) as json_file:
        try:
            json.dump(obj=json_dict, fp=json_file, skipkeys=True, indent=4)
        except Exception as excp:
            _logger.critical(
                'error "{error}" trying to write {text} JSON configuration to file "{file}"'.format(
                    error=excp, text=tmp_text, file=json_path
                )
            )
            sys.exit(EXT_ERR_WR_FILE)


################################################################################
def readJSON(
    json_path: FilePath, file_text: str = "", conf_file_name: str = ""
) -> object:
    """Reads the JSON from the given file and saves it to a class object with
    the JSON elements as attributes.

    If an error occurs, the program is exited with an error message!
    The JSON must have an element `file_version` that has a value of at least
    `CFG_VERSION`, if not, the program is exited with an error message.

    Args:
        json_path (FilePath): The path to the JSON file to read.
        file_text (str, optional): The name of the JSON configuration file for
                    logging proposes. Defaults to "", which will be logged as
                    'a', like in "Writing _a_ JSON configuration file ...".
        conf_file_name (str, optional): The string that has to be the value of
                    `file_name` in the JSON file, if not, the program exits.
                    Defaults to "".

    Returns:
        object: A class instance with the JSON elements as attributes.
    """
    _logger.warning(
        'Parsing {text} config file "{path}"'.format(text=file_text, path=json_path)
    )

    try:
        with io.open(json_path, mode="r", encoding="utf-8") as file:
            ret_val = json.load(file, object_hook=lambda dict: SimpleNamespace(**dict))

    except Exception as exp:
        _logger.critical(
            'error "{error}" parsing file "{path}"'.format(error=exp, path=json_path)
        )
        sys.exit(EXT_ERR_LD_FILE)

    try:
        checkConfigName(json_path, conf_file_name, ret_val)

        checkConfigVersion(json_path, ret_val)

    except Exception as excp:
        _logger.critical(
            'error "{error}" parsing file "{path}", JSON file not valid'.format(
                error=excp, path=json_path
            )
        )
        sys.exit(EXT_ERR_NOT_VLD)

    try:
        setOrigFile(json_path, ret_val)

    except Exception as excp:
        _logger.critical(
            'error "{error}" generating JSON file "{file}" checksum'.format(
                error=excp, file=json_path
            )
        )

    return ret_val


################################################################################
def setOrigFile(json_path: FilePath, ret_val: object) -> None:
    """Set the `FileCompare` instance `orig_file` to the original JSON configuration.

    Args:
        json_path (FilePath): The path to the JSON configuration file.
        ret_val (object): The deserialized JSON file.
    """
    if not hasattr(ret_val, "orig_file"):
        ret_val.orig_file = FileCompare(json_path)
    else:
        if ret_val.orig_file.path == json_path:
            ret_val.orig_file = FileCompare(json_path)
        else:
            # to get a FileCompare instance, not SimpleNamespace
            tmp_orig = FileCompare(ret_val.orig_file.path)
            tmp_orig.path = ret_val.orig_file.path
            tmp_orig.hash = ret_val.orig_file.hash
            tmp_orig.size = ret_val.orig_file.size
            ret_val.orig_file = tmp_orig


################################################################################
def checkConfigVersion(json_path: FilePath, ret_val: object) -> None:
    """Check the version of the JSON configuration file.

    Args:
        json_path (FilePath): The path to the JSON file.
        ret_val (object): The deserialized JSON configuration.
    """
    file_major, file_minor = ret_val.file_version.split(sep=".")
    if file_major < CFG_VERSION.major or file_minor < CFG_VERSION.minor:
        _logger.critical(
            'project file "{path}" is not a valid project file!'.format(path=json_path)
        )
        _logger.critical(
            'project file version (the value of \'file_version\') is too old. is "{old}" should be "{new}"'.format(
                old=ret_val.file_version, new=".".join(CFG_VERSION)
            )
        )
        sys.exit(EXT_ERR_NOT_VLD)


################################################################################
def checkConfigName(json_path: FilePath, conf_file_name: str, ret_val: object) -> None:
    """Check the name of the JSON configuration file.

    Args:
        json_path (FilePath): The path of the JSOn file to check.
        conf_file_name (str): The configuration name of the JSON file.
        ret_val (object): The deserialized JSON file.
    """
    if conf_file_name not in ("", ret_val.file_name):
        _logger.critical(
            'project file "{path}" is not a valid project file!'.format(path=json_path)
        )
        _logger.critical(
            'the value of \'file_name\' should be "{should}" but is "{but_is}"'.format(
                should=conf_file_name, but_is=ret_val.file_name
            )
        )
        sys.exit(EXT_ERR_NOT_VLD)
