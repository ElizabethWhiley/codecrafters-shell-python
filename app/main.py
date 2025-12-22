import os
import sys
import shlex
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
            with open(output_file, "w") as f:
                f.write(f"{command} {arguments}\n")
            continue

        if not command:
            continue

        if is_builtin(command):
            builtin_handlers[command](arguments)
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

if __name__ == "__main__":
    main()


# Parse an argument like this > and make it divert the output to a file
def parse_output_redirect(arguments: list[str]) -> tuple[list[str], str | None]:
    for i, arg in enumerate(arguments):
        if arg == ">":
            if i + 1 >= len(arguments):
                print(">: missing operand", flush=True)
                return arguments, None
            if arguments[i + 1].startswith(">"):
                print(">: cannot redirect output to a file that starts with >", flush=True)
                return arguments, None
            return arguments[:i], arguments[i + 1]
    return arguments, None
