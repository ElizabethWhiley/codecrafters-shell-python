import readline

class History:
    """Manages command history, integrating with readline for arrow key navigation."""

    def __init__(self):
        self.max_history_size = 100
        self.history = []

    def add(self, command: str) -> None:
        if command == "":
            return
        self.history.append(command)
        if len(self.history) > self.max_history_size:
            self.history.pop(0)
        readline.add_history(command)

    def get_all(self) -> list[str]:
        return self.history

    def get_last(self, n: int) -> list[str]:
        return self.history[-n:]

    def get_count(self) -> int:
        """Get the total number of history entries."""
        return len(self.history)

