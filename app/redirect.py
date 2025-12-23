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

