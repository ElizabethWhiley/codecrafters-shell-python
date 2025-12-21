import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    sys.stdout.write("$ ")
    # read the input from the user
    input = sys.stdin.readline()

    # and remove the newline character
    input = input.strip()
    sys.stdout.write(input + ": command not found")
    pass


if __name__ == "__main__":
    main()
