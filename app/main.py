import os
import sys
import shlex
import subprocess
from .builtin_commands import builtin_handlers, is_builtin
from .path_utils import get_executable_path


def main() -> None:
    while True:
        print(f"$ ", end="", flush=True)
        line = sys.stdin.readline().strip()
        # shlex.split handles shell-like parsing: quotes, escapes, preserved whitespace.
        # Special chars ($, *, ~) are treated as normal; adjacent quoted strings are concatenated.
        tokens = shlex.split(line) or [None]
        command, *arguments = tokens
        arguments, output_file = parse_output_redirect(arguments)
        if output_file:
            if is_builtin(command):
                output = builtin_handlers[command](arguments)
            elif get_executable_path(command):
                output = subprocess.run([command] + arguments, capture_output=True).stdout
            else:
                output = f"{command}: not found"
            with open(output_file, "w") as f:
                f.write(output)
            continue

        if not command:
            continue

        if is_builtin(command):
            output = builtin_handlers[command](arguments)
            print(output, flush=True)
            continue

        path = get_executable_path(command)
        if path:
            pid = os.fork()
            if pid == 0:
                os.execv(path, [command] + arguments)
            else:
                os.waitpid(pid, 0)
        else:
            print(f"{command}: not found", flush=True)


# Parse an argument like this > and make it divert the output to a file
def parse_output_redirect(arguments: list[str]) -> tuple[list[str], str | None]:
    for i, arg in enumerate(arguments):
        if arg == ">":
            if i + 1 >= len(arguments):
                return arguments, None
            output_file = arguments[i + 1]
            return arguments[:i], output_file
    return arguments, None


if __name__ == "__main__":
    main()


