import sys


def main():
    # read the input from the user and remove newline char
    valid = False
    while not valid:
        sys.stdout.write("$ ")
        input = sys.stdin.readline().strip()
        sys.stdout.write(input + ": command not found")
    pass


if __name__ == "__main__":
    main()
