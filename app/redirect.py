from dataclasses import dataclass
from enum import Enum, auto

class RedirectionType(Enum):
    FILE = auto()
    STDOUT = auto()
    STDERR = auto()
    APPEND = auto()
    AUTO = auto()

@dataclass
class Redirect:
    type: RedirectionType
    file: str | None = None

def parse_redirects(arguments: list[str]) -> tuple[Redirect, list[str]]:
    for i, arg in enumerate(arguments):
        type = parse_type(arg)
        if type != RedirectionType.AUTO:  # Found a redirect operator
            if i + 1 >= len(arguments):
                return Redirect(RedirectionType.AUTO), arguments
            # Return cleaned arguments (everything before the operator)
            return Redirect(type, arguments[i + 1]), arguments[:i]
    # No redirect found
    return Redirect(RedirectionType.AUTO, None), arguments

def parse_type(argument: str) -> RedirectionType:
    if argument == ">":
        return RedirectionType.FILE
    elif argument == "1>":
        return RedirectionType.STDOUT
    elif argument == "2>":
        return RedirectionType.STDERR
    elif argument == ">>":
        return RedirectionType.APPEND
    else:
        return RedirectionType.AUTO