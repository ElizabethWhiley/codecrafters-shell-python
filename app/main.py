import os
import sys

builtins = ["echo", "exit", "type"]

def main() -> None:
    while True:
        sys.stdout.write("$ ")
        input = sys.stdin.readline().strip()
        command = input.split()[0]
        arguments = input.split()[1:]
        if is_builtin(command):
            execute_builtin(command, arguments)
            continue

        path = get_executable_path(command)
        if path:
            execute_executable(command, path, arguments)
        else:
            sys.stdout.write(command + ": command not found\n")

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
    if command == "type":
        type_command(arguments)

    if command == "echo":
        sys.stdout.write(" ".join(arguments) + "\n")

    if command == "exit":
        sys.exit(0)

def execute_executable(command, path, arguments) -> None:
    os.execv(path, [command] + arguments)

def type_command(arguments) -> None:
    for arg in arguments:
        if is_builtin(arg):
            sys.stdout.write(arg + " is a shell builtin\n")
            continue

        path = get_executable_path(arg)
        if path:
            sys.stdout.write(arg + " is " + path + "\n")
        else:
            sys.stdout.write(arg + ": not found\n")

if __name__ == "__main__":
    main()
