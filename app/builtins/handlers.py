import os
import sys
from ..utils.path import get_executable_path

_current_history = None

def set_history(history):
    global _current_history
    _current_history = history

def _handle_cd(arguments: list[str], _stdin=None) -> str | None:
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

def _handle_exit(_arguments: list[str], _stdin=None) -> None:
    sys.exit(0)

def _handle_history(arguments: list[str], _stdin=None) -> str | None:
    if _current_history is None:
        return None

    if arguments:
        # check if it's a number or an "-r" flag

        if arguments[0] == "-r":
            # then checkif arguments[1] is the file path
            if len(arguments) < 2:
                return "history: -r requires a file path\n"
            file_path = arguments[1]
            # read the file line by line
            with open(file_path, "r") as file:
                for line in file:
                    stripped = line.strip()
                    if stripped:
                        _current_history.add(stripped)
            return None

        if arguments[0].isdigit():
            n = int(arguments[0])
            # current.history.get_last(n)
            # add line numbers
            output_lines = []
            last_n = _current_history.get_last(n)
            start_num = _current_history.get_count() - len(last_n) + 1
            for i, cmd in enumerate(last_n, start=start_num):
                output_lines.append(f"{i}  {cmd}\n")
            return "".join(output_lines)
    else:
        # current.history.get_last(10)
        output_lines = []
        last_10 = _current_history.get_last(10)
        start_num = _current_history.get_count() - len(last_10) + 1
        for i, cmd in enumerate(last_10, start=start_num):
            output_lines.append(f"{i}  {cmd}\n")
        return "".join(output_lines)

def _handle_pwd(_arguments: list[str], _stdin=None) -> str | None:
    return os.getcwd() + "\n"

def _process_type_line(line: str) -> str:
    """Helper to process a single line for type command."""
    line = line.strip()
    if not line:
        return ""
    if is_builtin(line):
        return f"{line} is a shell builtin\n"
    path = get_executable_path(line)
    if path:
        return f"{line} is {path}\n"
    return f"{line}: not found\n"

def _handle_type(arguments: list[str], stdin=None) -> str | None:
    output_lines = []

    # Arguments take precedence over stdin (like real shells)
    if arguments:
        for arg in arguments:
            output_lines.append(_process_type_line(arg))
    elif stdin:
        # Read from stdin only if no arguments
        try:
            # Try iterating line by line
            for line in stdin:
                result = _process_type_line(line)
                if result:
                    output_lines.append(result)
        except (AttributeError, TypeError):
            # Fallback: read all at once
            content = stdin.read() if hasattr(stdin, 'read') else str(stdin)
            for line in content.splitlines():
                result = _process_type_line(line)
                if result:
                    output_lines.append(result)

    return "".join(output_lines) if output_lines else None

builtin_handlers = {
    "cd": _handle_cd,
    "echo": _handle_echo,
    "exit": _handle_exit,
    "history": _handle_history,
    "pwd": _handle_pwd,
    "type": _handle_type,
}

def is_builtin(command: str) -> bool:
    return command in builtin_handlers
