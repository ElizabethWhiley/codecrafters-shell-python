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
        arguments, output_file = parse_file_redirect(arguments)
        if output_file:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            redirection_type = "file"
        else:
            redirection_type = "stdout"

        if command:
            if is_builtin(command):
                output = builtin_handlers[command](arguments)
                if redirection_type == "file":
                    with open(output_file, "w") as f:
                        f.write(output or "")
                else:
                    if output:
                        print(output, flush=True)
            elif (path := get_executable_path(command)):
                if redirection_type == "file":
                    with open(output_file, "w") as f:
                        print(f"DEBUG: Running {path} with arguments {arguments}", file=sys.stderr)
                        subprocess.run([path] + arguments, stdout=f, text=True)
                else:
                    pid = os.fork()
                    if pid == 0:
                        os.execv(path, [command] + arguments)
                    else:
                        os.waitpid(pid, 0)
            else:
                output = f"{command}: not found"
                if redirection_type == "file":
                    with open(output_file, "w") as f:
                        f.write(output)
                else:
                    print(output, flush=True)


# Parse an argument like this > and make it divert the output to a file
def parse_file_redirect(arguments: list[str]) -> tuple[list[str], str | None]:
    for i, arg in enumerate(arguments):
        if arg == ">":
            if i + 1 >= len(arguments):
                return arguments, None
            output_file = arguments[i + 1]
            return arguments[:i], output_file
    return arguments, None

if __name__ == "__main__":
    main()


