import shlex
from ..execution.command import Command
from ..execution.pipeline import Pipeline
from ..parsing.redirect_parser import RedirectParser

class ShellLineParser:
    def __init__(self, redirect_parser: RedirectParser):
        self.redirect_parser = redirect_parser

    def parse_line(self, line: str) -> Command | Pipeline:
        if "|" in line:
            return self._parse_pipeline(line)
        else:
            return self._parse_command(line)

    def _parse_pipeline(self, line: str) -> Pipeline:
        commands = line.split("|")
        return Pipeline([self._parse_command(command) for command in commands])

    def _parse_command(self, command: str) -> Command:
        tokens = shlex.split(command) or [None]
        command, *arguments = tokens
        redirect, cleaned_arguments = self.redirect_parser.parse_redirects(arguments)
        return Command(command, cleaned_arguments, redirect)

