from dataclasses import dataclass
from enum import Enum, auto

class RedirectionType(Enum):
    """Types of output redirection."""
    STDOUT = auto()
    STDERR = auto()
    AUTO = auto()

class FileMode(Enum):
    """File write modes (write or append)."""
    WRITE = "w"
    APPEND = "a"

@dataclass
class Redirect:
    """Represents output redirection configuration."""
    type: RedirectionType
    mode: FileMode
    file: str | None = None
