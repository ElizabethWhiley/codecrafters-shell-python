import shlex
from .command import Command
from .redirect import Redirect, RedirectionType, parse_redirects

def parse_command(line: str) -> Command:
    tokens = shlex.split(line) or [None]
    if len(tokens) == 0:
        return Command(None, [], Redirect(RedirectionType.AUTO, None))
    command, *arguments = tokens
    redirect, arguments = parse_redirects(arguments)
    return Command(command, arguments, redirect)
