import readline

class History:
    """Manages command history, using readline's native history."""

    def __init__(self):
        readline.set_history_length(100)

    def add(self, command: str) -> None:
        readline.add_history(command)

    def get_all(self) -> list[str]:
        length = readline.get_current_history_length()
        return [readline.get_history_item(i + 1) for i in range(length)]

    def get_last(self, n: int) -> list[str]:
        length = readline.get_current_history_length()
        start = max(1, length - n + 1)
        return [readline.get_history_item(i) for i in range(start, length + 1)]

    def get_count(self) -> int:
        return readline.get_current_history_length()

    def read_from_file(self, file_path: str) -> None:
        """Read history from a file and append to current history."""
        with open(file_path, "r") as file:
            for line in file:
                stripped = line.strip()
                if stripped:
                    readline.add_history(stripped)

    def write_to_file(self, file_path: str) -> None:
        """Write current history to a file."""
        with open(file_path, "w") as file:
            length = readline.get_current_history_length()
            for i in range(1, length + 1):
                file.write(readline.get_history_item(i) + "\n")

