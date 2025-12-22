import os
import sys

builtins = ["pwd","echo", "exit", "type"]

def main() -> None:
    while True:
        print("$ ", end="", flush=True)
        input = sys.stdin.readline().strip()
        command = input.split()[0]
        arguments = input.split()[1:]
        if is_builtin(command):
            execute_builtin(command, arguments)
            continue

        path = get_executable_path(command)
        if path:
            execute_executable(command, path, arguments)
            continue
        else:
            print(command + ": command not found", flush=True)

def is_builtin(command) -> bool:
    return command in builtins

def get_executable_path(command) -> str | None:
    paths = os.environ.get("PATH").split(":")
    for path in paths:
        if os.path.exists(os.path.join(path, command)):
            if os.access(os.path.join(path, command), os.X_OK):
                return os.path.join(path, command)
            else:
                continue
        else:
            continue
    return None

def execute_builtin(command, arguments) -> None:
    if command == "pwd":
        print(os.getcwd(), flush=True)
        return

    if command == "type":
        type_command(arguments)

    if command == "echo":
        print(" ".join(arguments), flush=True)

    if command == "exit":
        sys.exit(0)

def execute_executable(command, path, arguments) -> None:
    pid = os.fork()
    if pid == 0:
        os.execv(path, [command] + arguments)
    else:
        os.waitpid(pid, 0)

def type_command(arguments) -> None:
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
