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
                return self._handle_first_tab()
            elif self.tab_count == 2:
                return self._handle_second_tab()
        else:
            # Subsequent calls: handle cycling through matches
            return self._handle_cycling(state)

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

    def _handle_first_tab(self) -> str | None:
        """Handle first TAB press: ring bell, return match if single, None if multiple."""
        # Ring the bell
        sys.stderr.write('\x07')
        sys.stderr.flush()

        # If only one match, complete it immediately with trailing space
        if len(self.matches) == 1:
            return self.matches[0] + " "

        # Multiple matches: don't insert anything (just ring bell)
        # User presses TAB again to see all matches
        return None

    def _handle_second_tab(self) -> str | None:
        """Handle second TAB press: print all matches, don't insert anything."""
        # Sort matches alphabetically
        sorted_matches = sorted(self.matches)
        # Print matches separated by two spaces
        print("  ".join(sorted_matches))
        # Print newline after matches
        print()
        # Don't let readline insert anything
        return None

    def _handle_cycling(self, state: int) -> str | None:
        """Handle readline asking for more matches (state > 0)."""
        # For both first and second TAB, we don't want readline to cycle through matches
        # First TAB: we already returned None, so readline shouldn't call us with state>0
        # Second TAB: we printed all matches, so don't let readline insert anything
        return None