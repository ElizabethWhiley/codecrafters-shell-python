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

      HOW READLINE WORKS:
      - When user presses TAB, readline calls this function repeatedly with state=0, 1, 2, ...
      - state=0: "Give me the first match" (we fetch ALL matches here and return the first)
      - state=1: "Give me the second match" (we return matches[1])
      - state=2: "Give me the third match" (we return matches[2])
      - When we return None, readline stops asking and uses what we've given it

      Args:
          text: The prefix to complete (e.g., "ech" when user types "ech" + Tab)
          state: Index provided by readline (0 = first call, 1 = second, etc.)

      Returns:
          Completion string at index 'state', or None if no more matches
      """

      # ============================================================
      # STATE == 0: This is the FIRST call when TAB is pressed
      # ============================================================
      if state == 0:
          # Step 1: Find all possible matches (builtin commands + external executables)
          builtin_matches = get_builtin_completions(text)
          external_matches = get_external_completions(text)
          all_matches = builtin_matches + external_matches
          self.matches = list(dict.fromkeys(all_matches))  # Remove duplicates, keep order

          # Step 2: Track how many times TAB has been pressed for this prefix
          # If the prefix is the same as last time, increment tab_count (second TAB)
          # If the prefix changed, reset to 1 (first TAB for new prefix)
          if self.last_prefix == text:
              self.tab_count += 1  # Same prefix = second TAB press
          else:
              self.tab_count = 1   # New prefix = first TAB press
          self.last_prefix = text

          # Step 3: Handle FIRST TAB press (tab_count == 1)
          if self.tab_count == 1:
              # Ring the bell (makes a "ding" sound)
              sys.stderr.write('\x07')
              sys.stderr.flush()

              # If only ONE match exists, complete it immediately with a trailing space
              if len(self.matches) == 1:
                  return self.matches[0] + " "

              # If MULTIPLE matches exist, don't return anything (just ring bell)
              # This prevents readline from inserting anything. User presses TAB again to see all matches.
              if len(self.matches) > 1:
                  return None

          # Step 4: Handle SECOND TAB press (tab_count == 2)
          if self.tab_count == 2:
              # Sort matches alphabetically and print them all on one line
              self.matches = sorted(self.matches)
              print("  ".join(self.matches))  # Two spaces between each match
              # Print newline after matches
              print()
              # Return empty string to try to clear readline's buffer
              # (Python's readline doesn't have a direct way to clear/reset the line)
              return ""

      # ============================================================
      # STATE > 0: Readline is asking for MORE matches (cycling through)
      # ============================================================
      if state > 0:
          # If this is the FIRST TAB press with multiple matches, don't return anything
          # (we already rang the bell and returned None on state == 0)
          # This prevents readline from inserting matches on the first TAB
          if self.tab_count == 1:
              return None

          # If this is the SECOND TAB press, we've already printed all matches
          # Don't let readline insert anything - return None for all subsequent calls
          if self.tab_count == 2:
              return None