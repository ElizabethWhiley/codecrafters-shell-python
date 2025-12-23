import os
import subprocess
from .builtin_commands import builtin_handlers
from .path_utils import get_executable_path
from .redirect import Redirect, RedirectionType
from .output_handler import handle_output

def execute_builtin(command: str, arguments: list[str], redirect: Redirect) -> None:
  output = builtin_handlers[command](arguments)
  handle_output(output, redirect)

def execute_external(command: str, arguments: list[str], redirect: Redirect) -> None:
  path = get_executable_path(command)
  if not path:
    return execute_not_found(command, redirect)

  if redirect.type == RedirectionType.STDOUT or redirect.type == RedirectionType.STDERR:
    _execute_with_file_redirect(command, arguments, redirect, path)
  else:
    subprocess.run([command] + arguments, executable=path, text=True)

def execute_not_found(command: str, redirect: Redirect) -> None:
  output = f"{command}: not found\n"
  handle_output(output, redirect)

def _execute_with_file_redirect(command: str, arguments: list[str], redirect: Redirect, path: str) -> None:
  os.makedirs(os.path.dirname(redirect.file), exist_ok=True)
  with open(redirect.file, redirect.mode.value) as f:
    if redirect.type == RedirectionType.STDOUT:
      subprocess.run([command] + arguments, executable=path, stdout=f, text=True)
    elif redirect.type == RedirectionType.STDERR:
      subprocess.run([command] + arguments, executable=path, stderr=f, text=True)