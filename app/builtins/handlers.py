import os
import sys
from ..utils.path import get_executable_path

def _handle_cd(arguments: list[str], _stdin=None, context=None) -> str | None:
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
    if context:
        context.working_dir = os.getcwd()

def _handle_echo(arguments: list[str], stdin=None, context=None) -> str | None:
    if stdin and not arguments:
        # Read from stdin if no arguments
        return stdin.read()
    return " ".join(arguments) + "\n"

def _handle_exit(_arguments: list[str], _stdin=None, context=None) -> None:
    if context and context.history and context.history.histfile:
        context.history.write_to_file(context.history.histfile, mode="w")
    sys.exit(0)

def _handle_history(arguments: list[str], _stdin=None, context=None) -> str | None:
    if context is None or context.history is None:
        return None

    if not arguments:
        return context.history.format_default()

    flag_or_num = arguments[0]
    if flag_or_num in ["-r", "-w", "-a"]:
        if len(arguments) < 2:
            return f"history: {flag_or_num} requires a file path\n"

        file_path = arguments[1]
        if flag_or_num == "-r":
            context.history.read_from_file(file_path)
        elif flag_or_num == "-w":
            context.history.write_to_file(file_path, mode="w")
        elif flag_or_num == "-a":
            context.history.write_to_file(file_path, mode="a")
        return None

    if flag_or_num.isdigit():
        n = int(flag_or_num)
        return context.history.format_last_n(n)

    return None

def _handle_pwd(_arguments: list[str], _stdin=None, context=None) -> str | None:
    if context:
        return context.working_dir + "\n"
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

def _read_type_from_stdin(stdin) -> list[str]:
    """Read and process type commands from stdin."""
    results = []
    try:
        for line in stdin:
            result = _process_type_line(line)
            if result:
                results.append(result)
    except (AttributeError, TypeError):
        content = stdin.read() if hasattr(stdin, 'read') else str(stdin)
        for line in content.splitlines():
            result = _process_type_line(line)
            if result:
                results.append(result)
    return results

def _handle_type(arguments: list[str], stdin=None, context=None) -> str | None:
    output_lines = []

    if arguments:
        for arg in arguments:
            output_lines.append(_process_type_line(arg))
    elif stdin:
        output_lines = _read_type_from_stdin(stdin)

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
