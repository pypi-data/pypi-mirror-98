#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     buildnis.py
# Date:     13.Feb.2021
###############################################################################

from __future__ import annotations

import sys

from buildnis.modules import EXT_ERR_IMP_MOD

try:
    import logging
    import os
    from typing import List, Tuple
except ImportError as exp:
    print('ERROR: error "{error}" importing modules'.format(error=exp), file=sys.stderr)
    sys.exit(EXT_ERR_IMP_MOD)

try:
    from buildnis.modules import EXT_OK
    from buildnis.modules.config import (
        BUILD_TOOL_CONFIG_NAME,
        CFG_DIR_NAME,
        HOST_FILE_NAME,
        PROJECT_DEP_FILE_NAME,
        PROJECT_FILE_NAME,
        FilePath,
        config_values,
    )
    from buildnis.modules.config.config_dir_json import ConfigDirJson
    from buildnis.modules.config.config_files import ConfigFiles, ConfigTuple
    from buildnis.modules.config.configure_build import configureBuild
    from buildnis.modules.config.host import Host
    from buildnis.modules.helpers.commandline import parseCommandLine
    from buildnis.modules.helpers.commandline_arguments import (
        CommandlineArguments,
        doDistClean,
        setupLogger,
    )
    from buildnis.modules.helpers.files import checkIfIsFile
except ImportError as exp:
    print(
        'ERROR: error "{error}" importing own modules'.format(error=exp),
        file=sys.stderr,
    )
    sys.exit(EXT_ERR_IMP_MOD)


################################################################################
def main():
    """Main entry point of Buildnis.

    Parses commandline arguments and runs the program.
    """
    commandline_args = parseCommandLine()

    logger = setupLogger(commandline_args)

    project_cfg_dir = commandline_args.conf_dir

    project_cfg_dir, config_dir_config = setUpConfDir(
        commandline_args, logger, project_cfg_dir
    )

    # Always create host config
    host_cfg, host_cfg_filename = setUpHostCfg(logger, project_cfg_dir)

    json_config_files = setUpPaths(
        project_cfg_dir=project_cfg_dir,
        host_cfg_file=host_cfg_filename,
        list_of_generated_files=config_values.g_list_of_generated_files,
        host_cfg=host_cfg,
    )

    if not commandline_args.do_clean:
        configureBuild(
            commandline_args,
            logger,
            config_dir_config,
            host_cfg,
            host_cfg_filename,
            json_config_files,
        )

    else:
        logger.warning(
            'Not doing anything but deleting files, a "clean" argument ("--clean" or "--distclean") has been given!'
        )

    # ! WARNING: no more logging after this function!
    # Logger is shut down
    doDistClean(
        commandline_args=commandline_args,
        logger=logger,
        list_of_generated_files=config_values.g_list_of_generated_files,
        list_of_generated_dirs=config_values.g_list_of_generated_dirs,
    )

    sys.exit(EXT_OK)


################################################################################
def setUpConfDir(
    commandline_args: CommandlineArguments,
    logger: logging.Logger,
    project_cfg_dir: FilePath,
) -> Tuple[FilePath, ConfigDirJson]:
    """Set up the configuration directory.

    Args:
        commandline_args ([CommandlineArguments]): instance holding the command line
                        parameters, especially `commandline_args.project_config_file`.
        logger ([type]): The `logger.Logger` instance to use.
        project_cfg_dir ([FilePath]): Path to the configuration directory.

    Returns
        Tuple[FilePath, ConfigDirJson]: A Tuple containing the configuration directory
                                    and the `ConfigDirJson` instance to use.

    """
    working_dir = os.path.abspath(os.path.dirname(commandline_args.project_config_file))
    config_dir_filename = "/".join([working_dir, CFG_DIR_NAME])
    config_dir_filename = ".".join([config_dir_filename, "json"])
    config_dir_filename = os.path.abspath(config_dir_filename)
    config_dir_config = ConfigDirJson(
        file_name=config_dir_filename, working_dir=working_dir, cfg_path=project_cfg_dir
    )
    config_values.g_list_of_generated_files.append(config_dir_config.json_path)
    project_cfg_dir = config_dir_config.cfg_path
    if project_cfg_dir != working_dir:
        config_values.g_list_of_generated_dirs.append(project_cfg_dir)
    logger.info(
        'Setting project configuration directory to "{path}"'.format(
            path=project_cfg_dir
        )
    )
    return project_cfg_dir, config_dir_config


################################################################################
def setUpPaths(
    project_cfg_dir: FilePath,
    host_cfg_file: FilePath,
    list_of_generated_files: List[FilePath],
    host_cfg: Host,
) -> ConfigFiles:
    """Helper: set up all pathnames of JSON files.

    Args:
        project_cfg_dir (FilePath): The path to the directory the JSON files are
                                    generated in
        host_cfg (FilePath): The path to the generated host configuration JSON file
        list_of_generated_files (List[FilePath]): List of generated JSON files
        host_cfg (host_config.Host): host configuration object instance

    Returns:
        ConfigFiles: the paths to the JSON files and a bool that is `True` if the file
                     already has been created.
    """
    host_cfg_filename_exists = False
    try:
        if checkIfIsFile(host_cfg_file) is True:
            list_of_generated_files.append(host_cfg_file)
            host_cfg_filename_exists = True
    except Exception:  # nosec
        pass

    build_tools = setUpConfigFile(
        project_cfg_dir=project_cfg_dir,
        list_of_generated_files=list_of_generated_files,
        host_cfg=host_cfg,
        config_name=BUILD_TOOL_CONFIG_NAME,
    )

    project_dep = setUpConfigFile(
        project_cfg_dir=project_cfg_dir,
        list_of_generated_files=list_of_generated_files,
        host_cfg=host_cfg,
        config_name=PROJECT_DEP_FILE_NAME,
    )

    project_config = setUpConfigFile(
        project_cfg_dir=project_cfg_dir,
        list_of_generated_files=list_of_generated_files,
        host_cfg=host_cfg,
        config_name=PROJECT_FILE_NAME,
    )

    return ConfigFiles(
        host_cfg=ConfigTuple(path=host_cfg_file, exists=host_cfg_filename_exists),
        build_tools_cfg=build_tools,
        project_dep_cfg=project_dep,
        project_cfg=project_config,
    )


################################################################################
def setUpConfigFile(
    project_cfg_dir: FilePath,
    list_of_generated_files: List[FilePath],
    host_cfg: Host,
    config_name: str,
) -> ConfigTuple:
    """Set up each the path to each of the configuration files.

    Args:
        project_cfg_dir (FilePath): The path to the directory the JSON files are
                                    generated in
        host_cfg (FilePath): The path to the generated host configuration JSON file
        list_of_generated_files (List[FilePath]): List of generated JSON files
        host_cfg (Host): host configuration object instance
        config_name (str): The name of the config file to return the path of.

    Returns:
        ConfigTuple: The path to the configuration JSON file and `True`, if
                                this file already exists, `False` if it will be
                                generated.
    """
    config_filename_exists = False
    config_filename = "/".join([project_cfg_dir, host_cfg.host_name])
    config_filename = "_".join([config_filename, config_name])
    config_filename = ".".join([config_filename, "json"])
    config_filename = os.path.normpath(config_filename)
    try:
        if checkIfIsFile(config_filename) is True:
            list_of_generated_files.append(config_filename)
            config_filename_exists = True
    except Exception:  # nosec
        pass
    return ConfigTuple(path=config_filename, exists=config_filename_exists)


################################################################################
def setUpHostCfg(
    logger: logging.Logger,
    project_cfg_dir: FilePath,
) -> Tuple[Host, FilePath]:
    """Helper: Sets up the host's configuration.

    Is always generated.

    Args:
        list_of_generated_files (List[FilePath]): The list of generated files to add to
        logger (logging.Logger): The logger to use
        project_cfg_dir (FilePath): Path to the project config JSON file

    Returns:
        Tuple[Host, FilePath]: the host configuration object instance and the host
                    configuration's filename as a tuple
    """
    host_cfg = Host()

    host_cfg_filename = "/".join([project_cfg_dir, host_cfg.host_name])
    host_cfg_filename = "_".join([host_cfg_filename, HOST_FILE_NAME])
    host_cfg_filename = ".".join([host_cfg_filename, "json"])
    host_cfg_filename = os.path.normpath(host_cfg_filename)

    logger.debug('Host config: """{cfg}"""'.format(cfg=host_cfg))

    return host_cfg, host_cfg_filename


################################################################################
if __name__ == "__main__":
    # execute only if run as a script
    main()
