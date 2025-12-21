import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    sys.stdout.write("$ ")
    # read the input from the user and remove newline char
    input = sys.stdin.readline().strip()
    sys.stdout.write(input + ": command not found")
    pass


if __name__ == "__main__":
    main()
