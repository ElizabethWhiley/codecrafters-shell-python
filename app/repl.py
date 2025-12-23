import sys
import readline
from .command_parser import CommandParser
from .completion_utils import get_builtin_completions, get_external_completions

class Repl():
    def __init__(self, command_parser: CommandParser):
      self.command_parser = command_parser
      self.matches = []
      self.setup_completion()

    def setup_completion(self) -> None:
        readline.set_completer(self._get_completions)
        readline.parse_and_bind("tab: complete")

    def run(self) -> None:
        while True:
            print(f"$ ", end="", flush=True)
            line = input()
            command = self.command_parser.parse_line(line) if line else None
            if command:
                command.execute()

    def _get_completions(self, text: str, state: int) -> str | None:
      """
      Completer function for readline tab completion.

      How 'state' works:
      - state == 0: New completion request (user pressed Tab)
        → Fetch all matches and store them in self.matches
        → Return the first match (self.matches[0])
      - state == 1, 2, 3...: Subsequent calls for more matches
        → Return self.matches[state] if it exists
        → This allows cycling through multiple matches with repeated Tab presses
      - Return None: Signals no more matches available
        → Readline stops asking for more completions

      Args:
          text: The prefix to complete (e.g., "ech" when user types "ech" + Tab)
          state: Index of the completion request (0 = first, 1 = second, etc.)

      Returns:
          The completion string at index 'state', or None if no more matches
      """
      if state == 0:
          # New completion request - fetch all matches
          builtin_matches = get_builtin_completions(text)
          external_matches = get_external_completions(text)
          # Combine and store for subsequent state calls
          self.matches = builtin_matches + external_matches

      # Return the match at index 'state', or None if we've exhausted all matches
      if state < len(self.matches):
          return self.matches[state]
      return None