import os
import sys
from builtins import builtin_handlers, is_builtin
from path_utils import get_executable_path


def main() -> None:
    while True:
        print(f"$ ", end="", flush=True)
        line = sys.stdin.readline().strip().split()
        command, *arguments = line or (None, [])

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
