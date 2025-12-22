import os
import sys
from .path_utils import get_executable_path

def handle_cd(arguments: list[str]) -> None:
    if len(arguments) == 0:
        print("cd: missing argument", flush=True)
        return

    if arguments[0] == "~":
        arguments[0] = os.path.expanduser("~")
    elif arguments[0].startswith("~"):
        arguments[0] = os.path.expanduser(arguments[0])

    absolute_path = os.path.abspath(arguments[0])
    if not os.path.exists(absolute_path) or not os.path.isdir(absolute_path):
        print(f"cd: {arguments[0]}: No such file or directory", flush=True)
        return

    os.chdir(absolute_path)


def handle_echo(arguments: list[str]) -> None:
    return " ".join(arguments)

def handle_exit(arguments: list[str]) -> None:
    sys.exit(0)

def handle_ls(arguments: list[str]) -> None:
    return " ".join(os.listdir(os.getcwd()))

def handle_pwd(arguments: list[str]) -> None:
    return os.getcwd()

def handle_type(arguments: list[str]) -> None:
    for arg in arguments:
        if is_builtin(arg):
            return f"{arg} is a shell builtin"

        path = get_executable_path(arg)
        if path:
            return f"{arg} is {path}"

        else:
            return f"{arg}: not found"

def is_builtin(command: str) -> bool:
    return command in builtin_handlers

builtin_handlers = {
    "cd": handle_cd,
    "echo": handle_echo,
    "exit": handle_exit,
    "ls": handle_ls,
    "pwd": handle_pwd,
    "type": handle_type,
}