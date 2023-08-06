# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     files.py
# Date:     21.Feb.2021
###############################################################################

from __future__ import annotations

import hashlib
import logging
import os
import pathlib
from typing import List

from buildnis.modules import BuildnisException
from buildnis.modules.config import FilePath


class FileCompareException(BuildnisException):
    """Exception raised if a given file path can't be accessed or read to
    generate the hash.
    """


################################################################################
def checkIfExists(file: FilePath) -> bool:
    """Returns `True` if the given file exists.

    Args:
        file (FilePath): Path to the file to test

    Raises:
        FileCompareException: if something went wrong

    Returns:
        bool: `True``, if the file exists
              `False` else
    """
    try:
        tmp_path = os.path.abspath(file)

        tmp_path_obj = pathlib.Path(tmp_path)

        if tmp_path_obj.exists():
            return True

    except Exception as excp:
        raise FileCompareException(excp)

    return False


################################################################################
def checkIfIsFile(file: FilePath) -> bool:
    """Returns `True` if the given file exists and is a file.

    Args:
        file (FilePath): Path to the file to test

    Raises:
        FileCompareException: if something went wrong

    Returns:
        bool: `True``, if the file exists and is a file
              `False` else
    """
    try:
        tmp_path = os.path.abspath(file)

        tmp_path_obj = pathlib.Path(tmp_path)

        if tmp_path_obj.is_file():
            return True

    except Exception as excp:
        raise FileCompareException(excp)

    return False


################################################################################
def checkIfIsDir(directory: FilePath) -> bool:
    """Returns `True` if the given file exists and is a directory.

    Args:
        directory (FilePath): Path to the directory to test

    Raises:
        FileCompareException: if something went wrong

    Returns:
        bool: `True``, if the file exists and is a directory
              `False` else
    """
    try:
        tmp_path = os.path.abspath(directory)

        tmp_path_obj = pathlib.Path(tmp_path)

        if tmp_path_obj.is_dir():
            return True

    except Exception as excp:
        raise FileCompareException(excp)

    return False


################################################################################
def checkIfIsLink(link: FilePath) -> bool:
    """Returns `True` if the given file exists and is a symlink.

    Args:
        link (FilePath): Path to the file to test

    Raises:
        FileCompareException: if something went wrong

    Returns:
        bool: `True``, if the file exists and is a symlink
              `False` else
    """
    try:
        tmp_path = os.path.abspath(link)

        tmp_path_obj = pathlib.Path(tmp_path)

        if tmp_path_obj.is_symlink():
            return True

    except Exception as excp:
        raise FileCompareException(excp)

    return False


################################################################################
def makeDirIfNotExists(directory: FilePath) -> None:
    """Creates the directory `directory` if it doesn't exist yet.

    Args:
        directory (FilePath): the directory to create

    Raises:
        FileCompareException: if something goes wrong
    """
    try:
        dir_path_obj = pathlib.Path(directory)

        if dir_path_obj.exists() and not dir_path_obj.is_dir():
            raise FileCompareException(
                'error creating directory, "{path}" exists but is not a directory!'.format(
                    path=directory
                )
            )

        dir_path_obj.mkdir(parents=True, exist_ok=True)

    except Exception as excp:
        raise FileCompareException(excp)


################################################################################
def hashFile(file: FilePath) -> str:
    """Generates a BLAKE2 hash of the file with the given path.

    Returns the hash as a hex string.
    If something goes wrong, it returns an `FileCompareException` instance.

    Raises:
            FileCompareException: if something goes wrong

    Args:
        file (FilePath): the file to return the BLAKE2 hash of

    Returns:
        str: the hex hash of the file's contend
    """
    ret_val = ""
    try:
        hash_func = hashlib.blake2b()

        file_data = pathlib.Path(file).read_bytes()

        hash_func.update(file_data)

        ret_val = hash_func.hexdigest()
    except Exception as excp:
        raise FileCompareException(excp)

    return ret_val


################################################################################
def returnExistingFile(file_list: List[FilePath]) -> FilePath:
    """Returns the first existing path in the list of given paths, and `""`
    the empty string, if none of the paths points to an existing file.

    Raises:
            FileCompareException: if something goes wrong

    Args:
        file_list (List[FilePath]): The list of file paths to check for existence.

    Returns:
        FilePath: The first of the given file paths that exists as a file, the
                    empty string (`""`) if none exists.
    """
    ret_val = ""
    try:
        for path in file_list:
            if checkIfExists(path):
                return path
    except FileCompareException as excp:
        raise excp

    return ret_val


################################################################################
def deleteDirs(logger: logging.Logger, list_of_dirs: List[FilePath]) -> None:
    """Deletes all directories in the given list of directories.

    Attention: directory has to be empty!

    Raises:
            FileCompareException: if something goes wrong

    Args:
        logger (logging.Logger): The logger instance to use for logging.
        list_of_dirs (List[FilePath]): The list of directories to delete. As a list of
                                        paths to the directories to delete.
    """
    try:
        for dir_path in list_of_dirs:
            logger.warning('deleting directory "{name}"'.format(name=dir_path))
            pathlib.Path(dir_path).rmdir()
    except Exception as excp:
        raise FileCompareException(excp)


################################################################################
def deleteFiles(logger, list_of_files: List[FilePath]) -> None:
    """Deletes all files in the given list of files to delete.

    Raises:
            FileCompareException: if something goes wrong

    Args:
        logger ([type]): The logger instance to use for logging.
        list_of_files (List[FilePath]): The list of files to delete. As a list of file
                                                    paths to the files to delete.
    """
    try:
        for file_path in list_of_files:
            logger.warning('deleting file "{name}"'.format(name=file_path))
            pathlib.Path(file_path).unlink(missing_ok=True)
    except Exception as excp:
        raise FileCompareException(excp)
