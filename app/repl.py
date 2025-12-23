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
      if state != 0:
          return None

      self.matches = self._fetch_matches(text)
      self._update_tab_count(text)

      handlers = {1: self._handle_first_tab, 2: self._handle_second_tab}
      handler = handlers.get(self.tab_count)
      return handler(text) if handler else None

    def _fetch_matches(self, text: str) -> list[str]:
        """Find all possible matches (builtin + external commands)."""
        builtin_matches = get_builtin_completions(text)
        external_matches = get_external_completions(text)
        all_matches = builtin_matches + external_matches
        # Remove duplicates while preserving order (builtins first)
        return list(dict.fromkeys(all_matches))

    def _update_tab_count(self, text: str) -> None:
      self.tab_count = self.tab_count + 1 if self.last_prefix == text else 1
      self.last_prefix = text

    def _handle_first_tab(self, text: str) -> str | None:
      sys.stderr.write('\x07')
      sys.stderr.flush()

      if not self.matches:
          return None

      if len(self.matches) == 1:
          return self.matches[0] + " "

      # Multiple matches: find longest common prefix
      longest_prefix = self._find_longest_common_prefix(self.matches)
      return longest_prefix if len(longest_prefix) > len(text) else None

    def _handle_second_tab(self, text: str) -> str | None:
      """Handle second TAB press: print all matches, clear matches, return None."""
      # Sort matches alphabetically
      sorted_matches = sorted(self.matches)
      sys.stdout.write("\n" + "  ".join(sorted_matches) + "\n")
      sys.stdout.flush()
      # Print the prompt and current input
      line_buffer = readline.get_line_buffer()
      sys.stdout.write(f"$ {line_buffer}\n")
      sys.stdout.flush()
      # Clear matches so readline has nothing to insert
      self.matches = []
      # Return None to stop readline from asking for more
      return None

    def _find_longest_common_prefix(self, matches: list[str]) -> str:
      if not matches:
          return ""

      prefix = matches[0]
      for match in matches[1:]:
          while not match.startswith(prefix) and prefix:
              prefix = prefix[:-1]
      return prefix
