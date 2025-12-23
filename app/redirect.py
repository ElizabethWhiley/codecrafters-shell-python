from dataclasses import dataclass
from enum import Enum, auto

class RedirectionType(Enum):
    FILE = auto()
    STDOUT = auto()
    STDERR = auto()
    APPEND = auto()
    AUTO = auto()

class RedirectMode(Enum):
    WRITE = "w"
    APPEND = "a"

@dataclass
class Redirect:
    type: RedirectionType
    mode: RedirectMode
    file: str | None = None

def parse_redirects(arguments: list[str]) -> tuple[Redirect, list[str]]:
    for i, arg in enumerate(arguments):
        redirect_type, mode = _parse_redirect_type(arg)  # Unpack the tuple
        if redirect_type != RedirectionType.AUTO:  # Found a redirect operator
            if i + 1 >= len(arguments):
                return Redirect(RedirectionType.AUTO, RedirectMode.WRITE, None), arguments
            # Return cleaned arguments (everything before the operator)
            return Redirect(redirect_type, mode, arguments[i + 1]), arguments[:i]
    # No redirect found
    return Redirect(RedirectionType.AUTO, RedirectMode.WRITE, None), arguments

def _parse_redirect_type(argument: str) -> tuple[RedirectionType, RedirectMode]:
    # Map redirect operators to (type, mode) tuples
    redirect_map = {
        ">": (RedirectionType.STDOUT, RedirectMode.WRITE),
        "1>": (RedirectionType.STDOUT, RedirectMode.WRITE),
        "2>": (RedirectionType.STDERR, RedirectMode.WRITE),
        ">>": (RedirectionType.STDOUT, RedirectMode.APPEND),
        "1>>": (RedirectionType.STDOUT, RedirectMode.APPEND),
        "2>>": (RedirectionType.STDERR, RedirectMode.APPEND),
        "&>": (RedirectionType.AUTO, RedirectMode.WRITE),
        "&>>": (RedirectionType.AUTO, RedirectMode.APPEND),
    }
    return redirect_map.get(argument, (RedirectionType.AUTO, RedirectMode.WRITE))