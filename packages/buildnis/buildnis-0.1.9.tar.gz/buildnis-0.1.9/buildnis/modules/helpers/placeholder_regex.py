# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     placeholder_regex.py
# Date:     08.Mar.2021
###############################################################################

from __future__ import annotations

import datetime
import re

from buildnis.modules.config import (
    LINUX_OS_STRING,
    OSX_OS_STRING,
    WINDOWS_OS_STRING,
    config_values,
)

# regexes to use

project_root_regex = re.compile(r"\$\{(PROJECT_ROOT)\}")
"""Regex to find the placeholder `${PROJECT_ROOT}`.
"""

project_name_regex = re.compile(r"\$\{(PROJECT_NAME)\}")
"""Regex to find the placeholder `${PROJECT_NAME}`.
"""

project_version_regex = re.compile(r"\$\{(PROJECT_VERSION)\}")
"""Regex to find the placeholder `${PROJECT_VERSION}`.
"""

project_author_regex = re.compile(r"\$\{(PROJECT_AUTHOR)\}")
"""Regex to find the placeholder `${PROJECT_AUTHOR}`.
"""

project_company_regex = re.compile(r"\$\{(PROJECT_COMPANY)\}")
"""Regex to find the placeholder `${PROJECT_COMPANY}`.
"""

project_copyright_info_regex = re.compile(r"\$\{(PROJECT_COPYRIGHT_INFO)\}")
"""Regex to find the placeholder `${PROJECT_COPYRIGHT_INFO}`.
"""

project_web_url_regex = re.compile(r"\$\{(PROJECT_WEB_URL)\}")
"""Regex to find the placeholder `${PROJECT_WEB_URL}`.
"""

project_email_regex = re.compile(r"\$\{(PROJECT_EMAIL)\}")
"""Regex to find the placeholder `${PROJECT_EMAIL}`.
"""

project_cfg_dir_regex = re.compile(r"\$\{(PROJECT_CONFIG_DIR_PATH)\}")
"""Regex to find the placeholder `${PROJECT_CONFIG_DIR_PATH}`.
"""

host_os_regex = re.compile(r"\$\{(HOST_OS)\}")
"""Regex to find the placeholder `${HOST_OS}`.
"""

host_name_regex = re.compile(r"\$\{(HOST_NAME)\}")
"""Regex to find the placeholder `${HOST_NAME}`.
"""

host_cpu_arch_regex = re.compile(r"\$\{(HOST_CPU_ARCH)\}")
"""Regex to find the placeholder `${HOST_CPU_ARCH}`.
"""

host_num_cores_regex = re.compile(r"\$\{(HOST_NUM_CORES)\}")
"""Regex to find the placeholder `${HOST_NUM_CORES}`.
"""

host_num_log_cores_regex = re.compile(r"\$\{(HOST_NUM_LOG_CORES)\}")
"""Regex to find the placeholder `${HOST_NUM_LOG_CORES}`.
"""

os_name_windows_regex = re.compile(r"\$\{(OS_NAME_WINDOWS)\}")
"""Regex to find the placeholder `${OS_NAME_WINDOWS}`.
"""

os_name_linux_regex = re.compile(r"\$\{(OS_NAME_LINUX)\}")
"""Regex to find the placeholder `${OS_NAME_LINUX}`.
"""

os_name_osx_regex = re.compile(r"\$\{(OS_NAME_OSX)\}")
"""Regex to find the placeholder `${OS_NAME_OSX}`.
"""

current_time_regex = re.compile(r"\$\{(TIME)\}")
"""Regex to find the placeholder `${TIME}`.
"""

current_date_regex = re.compile(r"\$\{(DATE)\}")
"""Regex to find the placeholder `${DATE}`.
"""

current_year_regex = re.compile(r"\$\{(YEAR)}")
"""Regex to find the placeholder `${YEAR}`.
"""

current_month_regex = re.compile(r"\$\{(MONTH)}")
"""Regex to find the placeholder `${MONTH}`.
"""

current_day_regex = re.compile(r"\$\{(DAY)}")
"""Regex to find the placeholder `${DAY}`.
"""

placeholder_regex = re.compile(r"\$\{(.*)\}")
"""Regex to find general placefolders, of the form `${STRING}`, where string
is to be substituted for a value of another configuration item.
"""


############################################################################
def replaceConstants(item: str) -> str:
    """Replaces all known constants defined in `config_values.py` in the given string.

    These are placeholders like `${PROJECT_ROOT}`, `${PROJECT_NAME}`, ...

    Args:
        item (str): The string to parse for known constants.

    Returns:
        str: The substitution if a placeholder has been found, the unaltered
                string else.
    """
    ret_val = item

    ret_val = replaceProjectConstants(ret_val)

    ret_val = replaceHostConstants(ret_val)

    ret_val = replaceDateTimeConstants(ret_val)

    return ret_val


################################################################################
def replaceDateTimeConstants(ret_val: str) -> str:
    """Replaces date and time placeholders with the current date and/or time.

    Args:
        ret_val (str): The string to parse.

    Returns:
        str: The replaced date and or time if a match has been found, the original
            string `ret_val` else.
    """
    result = current_date_regex.search(ret_val)
    if result:
        now_date = datetime.now()
        ret_val = current_date_regex.sub(now_date.strftime("%d.%m.%Y"), ret_val)
    result = current_year_regex.search(ret_val)
    if result:
        now_date = datetime.now()
        ret_val = current_year_regex.sub(now_date.strftime("%Y"), ret_val)
    result = current_month_regex.search(ret_val)
    if result:
        now_date = datetime.now()
        ret_val = current_month_regex.sub(now_date.strftime("%m"), ret_val)
    result = current_day_regex.search(ret_val)
    if result:
        now_date = datetime.now()
        ret_val = current_day_regex.sub(now_date.strftime("%d"), ret_val)
    result = current_time_regex.search(ret_val)
    if result:
        now_time = datetime.now()
        ret_val = current_time_regex.sub(now_time.strftime("%H:%M:%S"), ret_val)
    return ret_val


################################################################################
def replaceHostConstants(ret_val: str) -> str:
    """Replaces host placeholders with the corresponding values.

    Args:
        ret_val (str): The string to parse.

    Returns:
        str: The replaced values if a match has been found, the original
            string `ret_val` else.
    """
    result = host_os_regex.search(ret_val)
    if result:
        ret_val = host_os_regex.sub(
            config_values.HOST_OS.replace("\\", "\\\\"), ret_val
        )
    result = host_name_regex.search(ret_val)
    if result:
        ret_val = host_name_regex.sub(
            config_values.HOST_NAME.replace("\\", "\\\\"), ret_val
        )
    result = host_cpu_arch_regex.search(ret_val)
    if result:
        ret_val = host_cpu_arch_regex.sub(
            config_values.HOST_CPU_ARCH.replace("\\", "\\\\"), ret_val
        )
    result = host_num_cores_regex.search(ret_val)
    if result:
        ret_val = host_num_cores_regex.sub(
            config_values.HOST_NUM_CORES.replace("\\", "\\\\"), ret_val
        )
    result = host_num_log_cores_regex.search(ret_val)
    if result:
        ret_val = host_num_log_cores_regex.sub(
            config_values.HOST_NUM_LOG_CORES.replace("\\", "\\\\"), ret_val
        )
    result = os_name_osx_regex.search(ret_val)
    if result:
        ret_val = os_name_osx_regex.sub(OSX_OS_STRING, ret_val)
    result = os_name_linux_regex.search(ret_val)
    if result:
        ret_val = os_name_linux_regex.sub(LINUX_OS_STRING, ret_val)
    result = os_name_windows_regex.search(ret_val)
    if result:
        ret_val = os_name_windows_regex.sub(WINDOWS_OS_STRING, ret_val)
    return ret_val


################################################################################
def replaceProjectConstants(ret_val: str) -> str:
    """Replaces all project constant placeholders.

    Args:
        ret_val (str): The string to parse for placeholders.

    Returns:
        str: If a project placeholder has been found, the replaced value, the original
            string `ret_val` else.
    """
    result = project_root_regex.search(ret_val)
    if result:
        ret_val = project_root_regex.sub(
            config_values.PROJECT_ROOT.replace("\\", "\\\\"), ret_val
        )
    result = project_name_regex.search(ret_val)
    if result:
        ret_val = project_name_regex.sub(
            config_values.PROJECT_NAME.replace("\\", "\\\\"), ret_val
        )
    result = project_version_regex.search(ret_val)
    if result:
        ret_val = project_version_regex.sub(
            config_values.PROJECT_VERSION.replace("\\", "\\\\"), ret_val
        )
    result = project_author_regex.search(ret_val)
    if result:
        ret_val = project_author_regex.sub(
            config_values.PROJECT_AUTHOR.replace("\\", "\\\\"), ret_val
        )
    result = project_company_regex.search(ret_val)
    if result:
        ret_val = project_company_regex.sub(
            config_values.PROJECT_COMPANY.replace("\\", "\\\\"), ret_val
        )
    result = project_copyright_info_regex.search(ret_val)
    if result:
        ret_val = project_copyright_info_regex.sub(
            config_values.PROJECT_COPYRIGHT_INFO.replace("\\", "\\\\"), ret_val
        )
    result = project_web_url_regex.search(ret_val)
    if result:
        ret_val = project_web_url_regex.sub(
            config_values.PROJECT_WEB_URL.replace("\\", "\\\\"), ret_val
        )
    result = project_email_regex.search(ret_val)
    if result:
        ret_val = project_email_regex.sub(
            config_values.PROJECT_EMAIL.replace("\\", "\\\\"), ret_val
        )
    result = project_cfg_dir_regex.search(ret_val)
    if result:
        ret_val = project_cfg_dir_regex.sub(
            config_values.PROJECT_CONFIG_DIR_PATH.replace("\\", "\\\\"), ret_val
        )
    return ret_val
