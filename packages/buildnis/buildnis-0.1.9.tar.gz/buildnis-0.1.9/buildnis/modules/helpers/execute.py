# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     execute.py
# Date:     21.Feb.2021
###############################################################################

from __future__ import annotations

import re
import subprocess  # nosec
from typing import List, NamedTuple

from buildnis.modules.config import CmdOutput, FilePath


class ExecuteException(Exception):
    """The Exception is thrown if the execution of the given commandline fails."""


class RunRegex(NamedTuple):
    """Class to hold a regex tuple to parse a command output with.

    Attributes:
        regex (str): The actual regex to use for parsing the output of the command.
        group (int): The match group of the regex to use for the result.
    """

    regex: str = ""
    group: int = 0


class ExeArgs(NamedTuple):
    """Class to hold the arguments needed to run a command.

    Attributes:
        exe (FilePath): The path to the executable to call.
        args (List[str]): The list of arguments to pass to the executable.
    """

    exe: FilePath = ""
    args: List[str] = None


class EnvArgs(NamedTuple):
    """Class to hold the arguments needed for the environment script of a command to
    run.

    Attributes:
        script (FilePath): The path to the environment script to run or source.
        args (List[str]): The arguments to pass to the environment script.
        do_source (bool):  If this is true, the environment script is sourced in the
                        current command interpreter and not executed.
    """

    script: FilePath = ""
    args: List[str] = None
    do_source: bool = False


################################################################################
def runCommand(
    exe_args: ExeArgs,
    env_args: EnvArgs = EnvArgs(script="", args=None, do_source=False),
) -> CmdOutput:
    """Executes the given command with the given arguments.

    The argument `exe_args.exe` is the executable's name or path, needed arguments can
    be passed in the list `exe_args.args`.
    In `env_args` the command to set up an environment can be given, with
    needed arguments to this environment script in the list `env_args.args`.

    Args:
        exe_args (ExeArgs): The name of the executable or path to the executable
                        to call and the arguments to pass to the executable.
        env_args (EnvArgs): The arguments needed for the environment script, if
                            applicable. Holds the command to call the environment script
                            in `env_args.script`, the arguments to call the environment
                            script with in `env_args.args` and if the environment script
                            has to be sourced instead of running it,
                            `env_args.do_source` ir `True`.

    Raises:
        ExecuteException: if something goes wrong

    Returns:
        CmdOutput: The output of the executed command as tuple (stdout, stderr)
    """
    if exe_args.args is None:
        exe_args_real = []
    else:
        exe_args_real = exe_args.args

    if env_args.args is None:
        env_args_real = []
    else:
        env_args_real = env_args.args

    cmd_line_args = []

    setEnv(exe_args, env_args, exe_args_real, env_args_real, cmd_line_args)

    if env_args.script == "" or not env_args.do_source:
        cmd_line_args.append(exe_args.exe)

        for arg in exe_args_real:
            if arg != "":
                cmd_line_args.append(arg)

    try:
        process_result = subprocess.run(  # nosec
            args=cmd_line_args,
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
    except Exception as excp:
        raise ExecuteException(excp)

    return CmdOutput(std_out=process_result.stdout, err_out=process_result.stderr)


################################################################################
def setEnv(
    exe_args: ExeArgs,
    env_args: EnvArgs,
    exe_args_real: List[str],
    env_args_real: List[str],
    cmd_line_args: List[str],
) -> None:
    """Set up the command line arguments for the environment script.

    Args:
        exe_args (ExeArgs): The object holding the needed arguments for the executable
                            itself.
        env_args (EnvArgs): The object holding the needed arguments to set the
                        environment for the executable.
        exe_args_real (List[str]): The real list of executable arguments to use.
        env_args_real (List[str]): The real list of environment arguments to use.
        cmd_line_args (List[str]): The list of arguments to pass to the command
                            interpreter.
    """
    if env_args.script != "":
        if env_args.do_source is True:
            cmd_line_args.append("bash")
            cmd_line_args.append("-c")
            source_cmd = "source " + env_args.script + " " + " ".join(env_args_real)
            source_cmd = source_cmd + " && " + exe_args.exe
            source_cmd = source_cmd + " " + " ".join(exe_args_real)
            cmd_line_args.append(source_cmd)
        else:
            cmd_line_args.append(env_args.script)
            for env_arg in env_args_real:
                cmd_line_args.append(env_arg)
            cmd_line_args.append("&&")


################################################################################
def doesExecutableWork(
    exe_args: ExeArgs,
    check_regex: RunRegex,
    env_args: EnvArgs = EnvArgs(script="", args=None, do_source=False),
) -> str:
    """Checks if the given command line works.

    Tries to run the command with the given arguments (see `runCommand`) and
    parses the output of the program, tries to match the given regex `check_regex`
    in the output (`stdout` and `stderr`) of the command. If the match group
    `regex_group` (defaults to 0, the whole regex) is found in the output, the
    function returns the matched string.

    Args:
        exe_args (ExeArgs): The name of the executable or path to the executable
                        to call and the arguments to pass to the executable.
        env_args (EnvArgs): The arguments needed for the environment script, if
                            applicable. Holds the command to call the environment script
                            in `env_args.script`, the arguments to call the environment
                            script with in `env_args.args` and if the environment script
                            has to be sourced instead of running it,
                            `env_args.do_source` ir `True`.
        env_args: (EnvArgs): The arguments needed to setup the environment for the
                            executable, if applicable. Defaults to ("", None, False).

    Raises:
        ExecuteException: if something goes wrong

    Returns:
        str: the matched string if the regex matches the output, the empty string
             '' otherwise.
    """
    ret_val = ""

    try:
        output = runCommand(exe_args=exe_args, env_args=env_args)

        run_regex = re.search(check_regex.regex, output.std_out)
        if run_regex is not None and run_regex.group(check_regex.group):
            ret_val = run_regex.group(check_regex.group)

        else:
            run_regex = re.search(check_regex.regex, output.err_out)
            if run_regex is not None and run_regex.group(check_regex.group):
                ret_val = run_regex.group(check_regex.group).strip()

    except Exception as excp:
        raise ExecuteException(excp)

    return ret_val
