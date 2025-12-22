import sys


def main():
    builtins = ["echo", "exit"]
    # read the input from the user and remove newline char
    while True:
        sys.stdout.write("$ ")
        input = sys.stdin.readline().strip()
        # if input == "exit":
        #     sys.exit(0)
        command = input.split()[0]
        arguments = input.split()[1:]

        if command in builtins:
            sys.stdout.write(command + " is a shell builtin\n")

        # if command == "echo":
        #     sys.stdout.write(" ".join(arguments) + "\n")
        else:
            sys.stdout.write(command + ": command not found\n")
    pass


if __name__ == "__main__":
    main()
