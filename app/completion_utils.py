import os
from .builtin_commands import builtin_handlers

def get_builtin_completions(prefix: str) -> list[str]:
    return [command for command in builtin_handlers.keys() if command.startswith(prefix)]


def get_external_completions(prefix: str) -> list[str]:
    return [command for command in os.listdir(os.getcwd()) if command.startswith(prefix)]