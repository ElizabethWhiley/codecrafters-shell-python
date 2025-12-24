import os
from ..models.redirect import Redirect, RedirectionType


def _ensure_directory_exists(filepath: str) -> None:
    """Ensure the directory for a filepath exists, creating it if necessary."""
    directory = os.path.dirname(filepath)
    if directory:  # Only create if directory path is not empty
        os.makedirs(directory, exist_ok=True)


def handle_output(output: str | None, redirect: Redirect) -> None:
    if redirect.type == RedirectionType.STDOUT:
        if redirect.file:
            _write_to_file(output or "", redirect.file, redirect.mode.value)
        else:
            _print_to_stdout(output)
    elif redirect.type == RedirectionType.STDERR:
        if redirect.file:
            _write_to_file("", redirect.file, redirect.mode.value)  # Empty file
        _print_to_stdout(output)  # Always print to stdout
    else:  # AUTO
        _print_to_stdout(output)

def _write_to_file(content: str, filepath: str, mode: str) -> None:
    _ensure_directory_exists(filepath)
    with open(filepath, mode, encoding="utf-8") as file:
        file.write(content)
        file.flush()

def _print_to_stdout(output: str | None) -> None:
    if output:
        print(output, end="", flush=True)
