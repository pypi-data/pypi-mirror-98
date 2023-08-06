# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     configure_build.py
# Date:     09.Mar.2021
###############################################################################

from __future__ import annotations

import logging
import pathlib

from buildnis.modules.config import FilePath, config_values
from buildnis.modules.config.check import Check
from buildnis.modules.config.config import Config
from buildnis.modules.config.config_dir_json import ConfigDirJson
from buildnis.modules.config.config_files import ConfigFiles
from buildnis.modules.config.host import Host
from buildnis.modules.config.project_dependency import ProjectDependency
from buildnis.modules.helpers.commandline_arguments import CommandlineArguments


################################################################################
def configureBuild(
    commandline_args: CommandlineArguments,
    logger: logging.Logger,
    config_dir_config: ConfigDirJson,
    host_cfg: Host,
    host_cfg_filename: FilePath,
    json_config_files: ConfigFiles,
) -> None:
    """Configures the build.

    Args:
        commandline_args (CommandlineArguments): The object holding the command line
                                                arguments.
        logger (logging.Logger): The logger instance to use.
        config_dir_config (ConfigDirJson): The object holding the path to the directory,
                                            all generated JSON files are written to.
        host_cfg (Host): The host configuration instance.
        host_cfg_filename (FilePath): Path to the host configuration JSON file to write.
        json_config_files (ConfigFiles): Holds paths to all JSON configuration files to
                                        write.
    """
    writeHostCfg(host_cfg, host_cfg_filename)
    if (
        not json_config_files.build_tools_cfg.exists
        or commandline_args.do_configure is True
    ):
        build_tool_cfg = writeBuildTools(
            commandline_args, logger, host_cfg, json_config_files
        )
    else:
        logger.warning(
            'JSON file "{path}" already exists, not checking for build tool configurations'.format(
                path=json_config_files.build_tools_cfg.path
            )
        )
        build_tool_cfg = Check(
            os_name=host_cfg.os,
            arch=host_cfg.cpu_arch,
            user_path=commandline_args.conf_scripts_dir,
            do_check=False,
        )
        build_tool_cfg.readJSON(json_path=json_config_files.build_tools_cfg.path)

    ifConfigureDeleteProjectJSON(commandline_args, logger, json_config_files)
    cfg = setupProjectCfg(commandline_args, json_config_files)
    if (
        not json_config_files.project_dep_cfg.exists
        or commandline_args.do_configure is True
    ):
        cfg.checkDependencies(force_check=True)
    else:
        logger.warning(
            'JSON file "{path}" already exists, not checking project dependencies'.format(
                path=json_config_files.project_dep_cfg.path
            )
        )
        cfg.checkDependencies(force_check=False)
    cfg.project_dep_cfg.writeJSON()
    if not json_config_files.project_dep_cfg.exists:
        config_values.g_list_of_generated_files.append(
            json_config_files.project_dep_cfg.path
        )

    cfg.searchBuildTools(build_tool_cfg)
    logger.debug('Project config: """{cfg}"""'.format(cfg=cfg))
    logger.debug(
        'Project dependency config: """{cfg}"""'.format(cfg=cfg.project_dep_cfg)
    )
    writeProjectJSON(host_cfg_filename, json_config_files, cfg)
    config_dir_config.writeJSON()


################################################################################
def setupProjectCfg(
    commandline_args: CommandlineArguments, json_config_files: ConfigFiles
) -> Config:
    """Sets up the project configuration, including the project dependency
    configuration.

    Args:
        commandline_args (CommandlineArguments): The object holding all command line
                                                    arguments.
        json_config_files (ConfigFiles): Holds the path to the project configuration
                                        JSON file's path.

    Returns:
        Config: The project config containing all values
    """
    cfg = Config(
        project_config=commandline_args.project_config_file,
        json_path=json_config_files.project_cfg.path,
    )
    cfg.project_dep_cfg = ProjectDependency(
        cfg.project_dependency_config,
        json_path=json_config_files.project_dep_cfg.path,
    )
    cfg.expandAllPlaceholders()
    return cfg


################################################################################
def writeHostCfg(host_cfg: Host, host_cfg_filename: FilePath) -> None:
    """Write the host configuration JSON file.

    Args:
        host_cfg (Host): The host configuration to save.
        host_cfg_filename (FilePath): The path of the JSON file to write to.
    """
    host_cfg.writeJSON(json_path=host_cfg_filename)
    config_values.g_list_of_generated_files.append(host_cfg_filename)


################################################################################
def writeProjectJSON(
    host_cfg_filename: FilePath, json_config_files: ConfigFiles, cfg: Config
) -> None:
    """Writes the project configuration JSON to disk.

    Args:
        host_cfg_filename (FilePath): Path to the host configuration.
        json_config_files (ConfigFiles): The object holding the path to the project
                                        configuration JSON to write.
        cfg (Config): The project configuration instance to write to disk.
    """
    cfg.setBuildToolCfgPath(json_config_files.build_tools_cfg.path)
    cfg.setHostConfigPath(host_cfg_filename)
    cfg.writeJSON()
    if not json_config_files.project_cfg.exists:
        config_values.g_list_of_generated_files.append(
            json_config_files.project_cfg.path
        )


################################################################################
def ifConfigureDeleteProjectJSON(
    commandline_args: CommandlineArguments,
    logger: logging.Logger,
    json_config_files: ConfigFiles,
) -> None:
    """Deletes the project configuration JSON if it exists and `--configure` has been
    called.

    Args:
        commandline_args (CommandlineArguments): The object holding the command line
                                                arguments
        logger (logging.Logger): THe logger to use.
        json_config_files (ConfigFiles): The path to the project configuration JSON and
                                            whether it exists.
    """
    if json_config_files.project_cfg.exists and commandline_args.do_configure is True:

        try:
            pathlib.Path(json_config_files.project_cfg.path).unlink()
            json_config_files.project_cfg.exists = False
        except Exception as excp:
            logger.error(
                'error "{error}" deleting generated project config file to reconfigure project'.format(
                    error=excp
                )
            )


################################################################################
def writeBuildTools(
    commandline_args: CommandlineArguments,
    logger: logging.Logger,
    host_cfg: Host,
    json_config_files: ConfigFiles,
) -> Check:
    """Writes the build tools configuration to disk.

    Args:
        commandline_args (CommandlineArguments): The object holding all command line
                                                    arguments.
        logger (logging.Logger): The logger to use.
        host_cfg (Host): The host configuration instance.
        json_config_files (ConfigFiles): Holds the Path to the build tools JSON
                                    configuration path, the path to write to.

    Returns:
        Check: The build tools configuration object to use.
    """
    check_buildtools = Check(
        os_name=host_cfg.os,
        arch=host_cfg.cpu_arch,
        user_path=commandline_args.conf_scripts_dir,
    )
    check_buildtools.writeJSON(json_path=json_config_files.build_tools_cfg.path)
    if not json_config_files.build_tools_cfg.exists:
        config_values.g_list_of_generated_files.append(
            json_config_files.build_tools_cfg.path
        )
    logger.debug('Build tool config: """{cfg}"""'.format(cfg=check_buildtools))

    return check_buildtools
