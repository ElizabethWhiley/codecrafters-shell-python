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
        else:
            sys.stdout.write(command + ": command not found\n")

def is_builtin(command):
    return command in builtins

def execute_builtin(command, arguments):
    if command == "type":
            for arg in arguments:
                if arg in builtins:
                    sys.stdout.write(arg + " is a shell builtin\n")
                else:
                    sys.stdout.write(arg + ": not found\n")

    if command == "echo":
        sys.stdout.write(" ".join(arguments) + "\n")

    if command == "exit":
        sys.exit(0)

if __name__ == "__main__":
    main()
