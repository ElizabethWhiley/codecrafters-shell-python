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

        Readline calls this repeatedly with state=0, 1, 2, ... until we return None.
        - state=0: First call - fetch matches and handle first/second TAB
        - state>0: Subsequent calls - cycle through matches (if allowed)
        """
        if state == 0:
            # First call: fetch matches and update tab count
            self.matches = self._fetch_matches(text)
            self._update_tab_count(text)

            # Handle based on which TAB press this is
            if self.tab_count == 1:
                return self._handle_first_tab(text)
            elif self.tab_count == 2:
                return self._handle_second_tab(text)
            else:
                return None
        else:
            return None

    def _fetch_matches(self, text: str) -> list[str]:
        """Find all possible matches (builtin + external commands)."""
        builtin_matches = get_builtin_completions(text)
        external_matches = get_external_completions(text)
        all_matches = builtin_matches + external_matches
        # Remove duplicates while preserving order (builtins first)
        return list(dict.fromkeys(all_matches))

    def _update_tab_count(self, text: str) -> None:
        """Track how many times TAB has been pressed for this prefix."""
        if self.last_prefix == text:
            # Same prefix = user pressed TAB again
            self.tab_count += 1
        else:
            # New prefix = first TAB press for this prefix
            self.tab_count = 1
        self.last_prefix = text

    def _handle_first_tab(self, text: str) -> str | None:
        """Handle first TAB press: ring bell, return match if single, empty string if multiple."""
        # Ring the bell
        sys.stderr.write('\x07')
        sys.stderr.flush()

        # If only one match, complete it immediately with trailing space
        if len(self.matches) == 1:
            return self.matches[0] + " "

        # Multiple matches: return empty string to prevent readline from storing matches
        # This tells readline "no completion" but we still ring the bell
        return ""

    def _handle_second_tab(self, text) -> str | None:
      """Handle second TAB press: print all matches, clear matches, return None."""
      # Sort matches alphabetically
      sorted_matches = sorted(self.matches)
      # Print matches separated by two spaces on their own line
      # Ensure it's a complete line with newline
      sys.stdout.write("\n" + "  ".join(sorted_matches) + "\n")
      sys.stdout.flush()
      # Print the prompt and current input
      line_buffer = readline.get_line_buffer()
      sys.stdout.write(f"$ {line_buffer}")
      sys.stdout.flush()
      # Clear matches so readline has nothing to insert
      self.matches = []
      # Return None to stop readline from asking for more
      return None