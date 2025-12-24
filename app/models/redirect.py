from dataclasses import dataclass
from enum import Enum, auto

class RedirectionType(Enum):
    """Types of output redirection."""
    FILE = auto()
    STDOUT = auto()
    STDERR = auto()
    APPEND = auto()
    AUTO = auto()

class RedirectMode(Enum):
    """File open modes for redirection."""
    WRITE = "w"
    APPEND = "a"

@dataclass
class Redirect:
    """Represents output redirection configuration."""
    type: RedirectionType
    mode: RedirectMode
    file: str | None = None
