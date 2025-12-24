from typing import TextIO, TYPE_CHECKING

if TYPE_CHECKING:
    from ..execution.command import Command


def build_subprocess_kwargs(
    command: "Command",
    stdin: TextIO | int | None = None,
    stdout: TextIO | int | None = None,
    stderr: TextIO | int | None = None
) -> dict:
    """Build subprocess arguments for external commands."""
    return {
        "args": [command.command] + command.arguments,
        "executable": command.executable_path,
        "text": True,
        "stdin": stdin,
        "stdout": stdout,
        "stderr": stderr,
    }
