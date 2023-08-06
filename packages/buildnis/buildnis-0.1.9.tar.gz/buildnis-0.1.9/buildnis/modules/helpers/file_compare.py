# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     file_compare.py
# Date:     09.Mar.2021
###############################################################################

from __future__ import annotations

import os
import pathlib

from buildnis.modules.config import FilePath
from buildnis.modules.helpers.files import FileCompareException, checkIfIsFile, hashFile


class FileCompare:
    """Holds information about a file to compare it to another version of itself
    to see if something has changed.

    Does the following to steps:
        * compares the file sizes, if they are the same
        * compares the Blake2 hashes of both files

    Attributes:
        path (FilePath): path to the file as string
        path_obj (pathlib.Path): the `Path` object of the file
        size (int): the size of the file in bytes (symlinks don't have a
                    meaningful size)
        hash (str): the BLAKE2 hash of the file's contend as a hex string.

    Methods:
        isSame (bool): returns true if `self` 'is' the same as the given file.
        generateHash (str): generates the hash of the file, saves it in
                         `hash` and returns it
    """

    ############################################################################
    def __init__(self, file: FilePath) -> None:
        """Initializes the `FileCompare` object using it's path.

        If the given path `file` isn't a file or is not accessible, an exception
        of type `FileCompareException` is thrown.

        Raises:
            FileCompareException: if something goes wrong

        Args:
            file (FilePath): The path to the file.
        """
        try:
            self.path = os.path.abspath(file)

            self.path_obj = pathlib.Path(self.path)

            if not self.path_obj.is_file():
                raise FileCompareException(
                    'file "{path}" does not exist or is not a file!'.format(
                        path=self.path
                    )
                )

            self.size = self.path_obj.stat().st_size

            self.hash = hashFile(self.path)

        except Exception as excp:
            raise FileCompareException(excp)

    ############################################################################
    def generateHash(self) -> str:
        """Rehashes the file, saves and returns the hash as hex string.

        The hash replaces the old one in the attribute `hash`.

        Raises:
            FileCompareException: if something goes wrong

        Returns:
            str: The hash of the file with path `path` as hex string.
        """
        return hashFile(self.path)

    ############################################################################
    def isSameFile(self, other: FileCompare) -> bool:
        """Checks whether two `FileComare` instances hold the same file content.


        Compares `self` against another FileCompare instance, comparing file size
        and hash.

        Returns `True` if both files have the same content.

        Attention: does NOT compare the filenames, only file size and hash of the
        files are compared.

        Args:
            other (FileCompare): the instance to compare `self` to

        Raises:
            FileCompareException: if something doesn't work out well ....

        Returns:
            bool: `True`, if both instances have the same filesize and hash.
                  `False` else
        """
        ret_val = self.size == other.size and self.hash == other.hash

        return ret_val

    ############################################################################
    def isSame(self, file: FilePath, not_exist_is_excp: bool = False) -> bool:
        """Checks whether `self` and the file with path `file` are the same.

        Problem: a symlink to the file and the file itself are NOT the same using
        this.

        Args:
            file (FilePath): path to the file to check
            not_exist_is_excp (bool): if this is `True` an exception is raised
                    if `file` does not exist. If this is `False`, `False` is
                    returned - the files data is not the same. Default: `False`

        Raises:
            FileCompareException: if something goes wrong

        Returns:
            bool:   `True`, if the file is the same
                    `False` else
        """
        try:
            tmp_path = os.path.abspath(file)

            tmp_path_obj = pathlib.Path(tmp_path)

            if not tmp_path_obj.is_file():
                if not_exist_is_excp is True:
                    raise FileCompareException(
                        'file "{path}" does not exist or is not a file!'.format(
                            path=tmp_path
                        )
                    )
                if not not_exist_is_excp:
                    return False

            tmp_size = tmp_path_obj.stat().st_size

            if self.size != tmp_size:
                return False

            tmp_hash = hashFile(tmp_path)

            if self.hash != tmp_hash:
                return False

        except Exception as excp:
            raise FileCompareException(excp)

        return True

    ############################################################################
    def hasChanged(self, not_exist_is_excp: bool = False) -> bool:
        """Checks if the stored file has changed on disk since taking the last
        checksum.

        If the file has changed (another file size or checksum) or it doesn't
        exist any more, `True` is returned. If the file still has the same
        checksum as the stored one, `False` is returned.

        Args:
            not_exist_is_excp (bool, optional): Should an exception be raised if
                                    the file doesn't exist anymore? Defaults to
                                    False.

        Raises:
            FileCompareException:  if something went wrong

        Returns:
            bool: `True`, if the file has changed since calculating the checksum,
                    `False` else.
        """
        try:
            if not checkIfIsFile(self.path):
                if not_exist_is_excp is True:
                    raise FileCompareException(
                        'file "{path}" does not exist or is not a file!'.format(
                            path=self.path
                        )
                    )
                if not not_exist_is_excp:
                    return True
            else:
                file_size_now = self.path_obj.stat().st_size
                if file_size_now != self.size:
                    return True
                hash_now = hashFile(self.path)
                if hash_now != self.hash:
                    return True

                return False

        except Exception as excp:
            raise FileCompareException(excp)


################################################################################
def areHashesSame(
    file1: FilePath, file2: FilePath, not_exist_is_excp: bool = False
) -> bool:
    """Compares the BLAKE2 hashes of the given files.

    Returns `True` if the contents of both files are the same (have the same hash).

    Args:
        file1 (FilePath): first file to compare
        file2 (FilePath): second file to compare
        not_exist_is_excp (bool): if this is `True` an exception is raised
                    if a file does not exist. If this is `False`, `False` is
                    returned - the files hashes are not the same. Default: `False`

    Raises:
        FileCompareException: if something goes wrong

    Returns:
        bool: `True`, if both files' content have the same BLAKE2 hash value.
              `False` else
    """
    try:
        if not checkIfIsFile(file1):
            if not_exist_is_excp is True:
                raise FileCompareException(
                    'file "{path}" does not exist or is not a file!'.format(path=file1)
                )
            if not not_exist_is_excp:
                return False

        if not checkIfIsFile(file2):
            if not_exist_is_excp is True:
                raise FileCompareException(
                    'file "{path}" does not exist or is not a file!'.format(path=file2)
                )
            if not not_exist_is_excp:
                return False

        file_size1 = pathlib.Path(file1).stat().st_size
        file_size2 = pathlib.Path(file2).stat().st_size

        if file_size1 != file_size2:
            return False

        hash1 = hashFile(file1)
        hash2 = hashFile(file2)

        return hash1 == hash2

    except Exception as excp:
        raise FileCompareException(excp)
