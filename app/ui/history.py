import os
import readline

# Constants
DEFAULT_HISTORY_LENGTH = 100
DEFAULT_HISTORY_COUNT = 10

class History:
    """Manages command history, using readline's native history."""

    def __init__(self):
        readline.set_history_length(DEFAULT_HISTORY_LENGTH)
        self._last_written_count = 0
        self._histfile = None

        histfile = os.environ.get("HISTFILE")
        if histfile:
            if not os.path.exists(histfile):
                raise FileNotFoundError(f"HISTFILE={histfile}: No such file or directory")
            self._histfile = histfile
            self.read_from_file(histfile)
            self._last_written_count = self.get_count()

    def get_histfile(self) -> str | None:
        """Get the history file path if set via HISTFILE env var."""
        return self._histfile

    def add(self, command: str) -> None:
        readline.add_history(command)

    def get_all(self) -> list[str]:
        length = readline.get_current_history_length()
        return [readline.get_history_item(i + 1) for i in range(length)]

    def get_last(self, count: int) -> list[str]:
        length = readline.get_current_history_length()
        start = max(1, length - count + 1)
        return [readline.get_history_item(i) for i in range(start, length + 1)]

    def get_count(self) -> int:
        return readline.get_current_history_length()

    def format_with_line_numbers(self, items: list[str], start_num: int) -> str:
        """Format history items with line numbers."""
        output_lines = []
        for i, cmd in enumerate(items, start=start_num):
            output_lines.append(f"{i}  {cmd}\n")
        return "".join(output_lines)

    def format_last_n(self, count: int) -> str:
        """Get last n history items and format them with line numbers."""
        last_n = self.get_last(count)
        start_num = self.get_count() - len(last_n) + 1
        return self.format_with_line_numbers(last_n, start_num)

    def format_default(self) -> str:
        """Format last 10 history items with line numbers."""
        return self.format_last_n(DEFAULT_HISTORY_COUNT)

    def read_from_file(self, file_path: str) -> None:
        """Read history from a file and append to current history."""
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                stripped = line.strip()
                if stripped:
                    readline.add_history(stripped)

    def write_to_file(self, file_path: str, mode: str = "w") -> None:
        """Write current history to a file.

        Args:
            file_path: Path to the history file
            mode: File mode - "w" for write (overwrite), "a" for append (only new entries)
        """
        length = readline.get_current_history_length()
        start = 1 if mode == "w" else self._last_written_count + 1

        with open(file_path, mode, encoding="utf-8") as file:
            for i in range(start, length + 1):
                file.write(readline.get_history_item(i) + "\n")

        self._last_written_count = length
