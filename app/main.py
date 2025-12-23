import sys
from .parser import parse_command

def main() -> None:
    while True:
        print(f"$ ", end="", flush=True)
        line = sys.stdin.readline().strip()
        command = parse_command(line) if line else None
        if command:
            command.execute()

if __name__ == "__main__":
    main()


