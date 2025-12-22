import os
import sys
from .builtin_commands import builtin_handlers, is_builtin
from .path_utils import get_executable_path


def main() -> None:
    while True:
        print(f"$ ", end="", flush=True)
        line = sys.stdin.readline().strip()
        command, *arguments = parse_arguments(line)

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


def parse_arguments(line: str) -> list[str]:
    if line.startswith("'"):
        return [line[1:-1]]
    if line.startswith('"'):
        return [line[1:-1]]
    return line.split()
