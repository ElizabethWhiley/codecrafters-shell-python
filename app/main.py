import os
import sys
import shlex
from .builtin_commands import builtin_handlers, is_builtin
from .path_utils import get_executable_path


def main() -> None:
    while True:
        print(f"$ ", end="", flush=True)
        line = sys.stdin.readline().strip()
        # shlex.split will return a list of tokens, or [None] if the line is empty
        tokens = shlex.split(line) or [None]
        # tokens is a list of strings, or [None] if the line is empty
        command, *arguments = tokens # unpack the list into command and arguments

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


