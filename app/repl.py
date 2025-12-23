import sys
import readline
from .command_parser import CommandParser
from .completion_utils import get_builtin_completions, get_external_completions

class Repl():
    def __init__(self, command_parser: CommandParser):
      self.command_parser = command_parser
      self.matches = []
      self.setup_completion()
      self.last_prefix = ""
      self.tab_count = 0

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

      Readline automatically calls this with state=0, 1, 2, ... until None is returned.
      - state == 0: Fetch all matches and store in self.matches, return first match
      - state > 0: Return self.matches[state] if it exists, else None (signals end)

      Args:
          text: The prefix to complete (e.g., "ech" when user types "ech" + Tab)
          state: Index provided by readline (0 = first call, 1 = second, etc.)

      Returns:
          Completion string at index 'state', or None if no more matches
      """
      if state == 0:
          # New completion request - fetch all matches
          builtin_matches = get_builtin_completions(text)
          external_matches = get_external_completions(text)
          # Combine: builtins first (prioritized), then externals, remove duplicates
          # Use dict.fromkeys to preserve order: builtins come before externals
          all_matches = builtin_matches + external_matches
          self.matches = list(dict.fromkeys(all_matches))

          if self.last_prefix == text:
            self.tab_count += 1
          else:
            self.tab_count = 1  # First TAB press for this prefix
          self.last_prefix = text

          # Add trailing space if exactly one match
          if len(self.matches) == 1:
              self.matches[0] = self.matches[0] + " "

      # Return the match at index 'state', or None if we've exhausted all matches
      if state < len(self.matches):
          return self.matches[state]
      return None