import os
import sys

builtins = ["pwd", "echo", "exit", "type"]

def main() -> None:
    while True:
        print(f"$ ", end="", flush=True)
        line = sys.stdin.readline().strip().split()
        command, *arguments = line or (None, [])

        if not command:
            continue

        if is_builtin(command):
            execute_builtin(command, arguments)
            continue

        path = get_executable_path(command)
        if path:
            execute_executable(command, path, arguments)
            continue

        print(f"{command}: command not found", flush=True)

def is_builtin(command: str) -> bool:
    return command in builtins

def get_executable_path(command: str) -> str | None:
    paths = os.environ.get("PATH").split(":")
    for path_dir in paths:
        joined_path = os.path.join(path_dir, command)
        if os.path.exists(joined_path) and os.access(joined_path, os.X_OK):
            return joined_path
    return None

def execute_builtin(command: str, arguments: list[str]) -> None:
    if command == "cd":
        if arguments[0].startswith("/") and os.path.exists(arguments[0]):
            os.chdir(arguments[0])
        else:
            print(f"cd: {arguments[0]}: No such file or directory", flush=True)
        return

    if command == "ls":
        print(os.listdir(os.getcwd()), flush=True)
        return

    if command == "pwd":
        print(os.getcwd(), flush=True)
        return

    if command == "type":
        type_command(arguments)

    if command == "echo":
        print(" ".join(arguments), flush=True)

    if command == "exit":
        sys.exit(0)

def execute_executable(command: str, path: str, arguments: list[str]) -> None:
    pid = os.fork()
    if pid == 0:
        os.execv(path, [command] + arguments)
    else:
        os.waitpid(pid, 0)

def type_command(arguments: list[str]) -> None:
    for arg in arguments:
        if is_builtin(arg):
            print(arg + " is a shell builtin", flush=True)
            continue

        path = get_executable_path(arg)
        if path:
            print(arg + " is " + path, flush=True)

        else:
            print(arg + ": not found", flush=True)

if __name__ == "__main__":
    main()
