import os
import sys
from ..utils.path import get_executable_path

def _handle_cd(arguments: list[str], stdin=None) -> str | None:
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

def _handle_echo(arguments: list[str], stdin=None) -> str | None:
    if stdin and not arguments:
        # Read from stdin if no arguments
        return stdin.read()
    return " ".join(arguments) + "\n"

def _handle_exit(arguments: list[str], stdin=None) -> None:
    sys.exit(0)

def _handle_pwd(arguments: list[str], stdin=None) -> str | None:
    return os.getcwd() + "\n"

def _handle_type(arguments: list[str], stdin=None) -> str | None:
    output_lines = []

    if stdin:
        # Read from stdin, process each line
        try:
            for line in stdin:
                line = line.strip() if isinstance(line, str) else line.rstrip('\n\r')
                if not line:
                    continue
                if is_builtin(line):
                    output_lines.append(f"{line} is a shell builtin\n")
                else:
                    path = get_executable_path(line)
                    if path:
                        output_lines.append(f"{line} is {path}\n")
                    else:
                        output_lines.append(f"{line}: not found\n")
        except (AttributeError, TypeError):
            # stdin might not be iterable, try reading all at once
            content = stdin.read() if hasattr(stdin, 'read') else str(stdin)
            for line in content.splitlines():
                line = line.strip()
                if not line:
                    continue
                if is_builtin(line):
                    output_lines.append(f"{line} is a shell builtin\n")
                else:
                    path = get_executable_path(line)
                    if path:
                        output_lines.append(f"{line} is {path}\n")
                    else:
                        output_lines.append(f"{line}: not found\n")
    else:
        # Use arguments (original behavior)
        for arg in arguments:
            if is_builtin(arg):
                output_lines.append(f"{arg} is a shell builtin\n")
            else:
                path = get_executable_path(arg)
                if path:
                    output_lines.append(f"{arg} is {path}\n")
                else:
                    output_lines.append(f"{arg}: not found\n")

    return "".join(output_lines) if output_lines else None

builtin_handlers = {
    "cd": _handle_cd,
    "echo": _handle_echo,
    "exit": _handle_exit,
    "pwd": _handle_pwd,
    "type": _handle_type,
}

def is_builtin(command: str) -> bool:
    return command in builtin_handlers
