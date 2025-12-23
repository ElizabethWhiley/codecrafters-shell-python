import os
import sys
from ..utils.path import get_executable_path

def _handle_cd(arguments: list[str]) -> str | None:
    if len(arguments) == 0:
        return "cd: missing argument\n"

    if arguments[0] == "~":
        arguments[0] = os.path.expanduser("~")
    elif arguments[0].startswith("~"):
        arguments[0] = os.path.expanduser(arguments[0])

    absolute_path = os.path.abspath(arguments[0])
    if not os.path.exists(absolute_path) or not os.path.isdir(absolute_path):
        return f"cd: {arguments[0]}: No such file or directory\n"

    os.chdir(absolute_path)

def _handle_echo(arguments: list[str]) -> str | None:
    return " ".join(arguments) + "\n"

def _handle_exit(arguments: list[str]) -> None:
    sys.exit(0)

def _handle_pwd(arguments: list[str]) -> str | None:
    return os.getcwd() + "\n"

def _handle_type(arguments: list[str]) -> str | None:
    for arg in arguments:
        if is_builtin(arg):
            return f"{arg} is a shell builtin\n"

        path = get_executable_path(arg)
        if path:
            return f"{arg} is {path}\n"

        else:
            return f"{arg}: not found\n"

builtin_handlers = {
    "cd": _handle_cd,
    "echo": _handle_echo,
    "exit": _handle_exit,
    "pwd": _handle_pwd,
    "type": _handle_type,
}

def is_builtin(command: str) -> bool:
    return command in builtin_handlers

