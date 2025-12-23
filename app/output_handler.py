import os
from .redirect import Redirect, RedirectionType

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
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode) as f:
        f.write(content)
        f.flush()

def _print_to_stdout(output: str | None) -> None:
    if output:
        print(output, end="", flush=True)