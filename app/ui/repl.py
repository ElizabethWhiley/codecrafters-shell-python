import sys
import readline
from ..parsing.shell_parser import ShellLineParser
from ..utils.completion import get_all_completions, get_completion_result
from .history import History
from ..models.shell_context import ShellContext

class Repl():
    def __init__(self, command_parser: ShellLineParser):
      self.command_parser = command_parser
      self.matches = []
      self._setup_completion()
      self.last_prefix = ""
      self.tab_count = 0
      self.history = History()
      self.context = ShellContext(self.history)

    def _setup_completion(self) -> None:
        readline.set_completer(self._get_completions)
        readline.parse_and_bind("tab: complete")
        readline.set_auto_history(True)

    def run(self) -> None:
        while True:
            line = input("$ ")
            result = self.command_parser.parse_line(line) if line else None
            if result:
                result.execute(context=self.context)

    def _get_completions(self, text: str, state: int) -> str | None:
      if state != 0:
          return None

      self.matches = get_all_completions(text)
      self._update_tab_count(text)

      if self.tab_count == 1:
          return self._handle_first_tab(text)
      elif self.tab_count == 2:
          return self._handle_second_tab()
      return None

    def _update_tab_count(self, text: str) -> None:
      self.tab_count = self.tab_count + 1 if self.last_prefix == text else 1
      self.last_prefix = text

    def _ring_bell(self) -> None:
      sys.stderr.write('\x07')
      sys.stderr.flush()

    def _print_matches(self) -> None:
      """Print all matches separated by two spaces."""
      sorted_matches = sorted(self.matches)
      sys.stdout.write("\n" + "  ".join(sorted_matches) + "\n")
      sys.stdout.flush()

    def _print_prompt(self) -> None:
      """Print the prompt and current input line."""
      line_buffer = readline.get_line_buffer()
      sys.stdout.write(f"$ {line_buffer}\n")
      sys.stdout.flush()

    def _handle_first_tab(self, text: str) -> str | None:
      self._ring_bell()
      return get_completion_result(self.matches, text)

    def _handle_second_tab(self) -> str | None:
      """Handle second TAB press: print all matches, clear matches, return None."""
      self._print_matches()
      self._print_prompt()
      self.matches = []
      return None

