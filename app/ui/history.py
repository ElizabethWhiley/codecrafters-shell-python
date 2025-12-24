import readline

class History:
    """Manages command history, using readline's native history."""

    def __init__(self):
        readline.set_history_length(100)

    def get_all(self) -> list[str]:
        length = readline.get_current_history_length()
        return [readline.get_history_item(i + 1) for i in range(length)]

    def get_last(self, n: int) -> list[str]:
        length = readline.get_current_history_length()
        start = max(1, length - n + 1)
        return [readline.get_history_item(i) for i in range(start, length + 1)]

    def get_count(self) -> int:
        return readline.get_current_history_length()

