import os
import sys

builtins = ["echo", "exit", "type"]

def main():
    while True:
        sys.stdout.write("$ ")
        input = sys.stdin.readline().strip()
        command = input.split()[0]
        arguments = input.split()[1:]
        if is_builtin(command):
            execute_builtin(command, arguments)
        elif is_executable(command):
            execute_executable(command, arguments)
        else:
            sys.stdout.write(command + ": command not found\n")

def is_builtin(command):
    return command in builtins

def is_executable(command):
    paths = os.environ.get("PATH").split(":")
    for path in paths:
        full_path = os.path.join(path, command)
        if os.path.exists(full_path):
            if os.access(full_path, os.X_OK):
                print("Found executable: " + full_path)
                return True
            else:
                continue
        else:
            continue
    return False

def execute_builtin(command, arguments):
    if command == "type":
        type_command(arguments)

    if command == "echo":
        sys.stdout.write(" ".join(arguments) + "\n")

    if command == "exit":
        sys.exit(0)

def execute_executable(command, arguments):
    pass

def type_command(arguments):
    for arg in arguments:
        if is_builtin(arg):
            sys.stdout.write(arg + " is a shell builtin\n")
        elif is_executable(arg):
            sys.stdout.write(arg + " is " + os.path.abspath(arg) + "\n")
        else:
            sys.stdout.write(arg + ": not found\n")

if __name__ == "__main__":
    main()
