import shlex
from .command import Command
from .redirect_parser import RedirectParser

class CommandParser:
  def __init__(self, redirect_parser: RedirectParser):
    self.redirect_parser = redirect_parser

  def parse_line(self, line: str) -> Command:
    tokens = shlex.split(line) or [None]
    if len(tokens) == 0:
        redirect, cleaned_arguments = self.redirect_parser.parse_redirects([])
        return Command(None, cleaned_arguments, redirect)
    command, *arguments = tokens
    redirect, cleaned_arguments = self.redirect_parser.parse_redirects(arguments)
    return Command(command, cleaned_arguments, redirect)
