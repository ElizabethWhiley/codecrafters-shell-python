import sys
from .parser import parse_command

class Repl():
    def __init__(self, builtin_handlers: dict[str, callable], parser_func):
      self.builtin_handlers = builtin_handlers
      self.parser = parser_func
      self._setup_completion()

    def run(self) -> None:
        while True:
            print(f"$ ", end="", flush=True)
            line = self._read_line()
            command = self.parser(line) if line else None
            if command:
                command.execute()

    def _setup_completion(self) -> None:
        # Setup tab completion (will add this)
        pass

    def _read_line(self) -> str:
        return sys.stdin.readline().strip()