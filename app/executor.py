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
  if path:
    if redirect.type == RedirectionType.STDOUT:
      os.makedirs(os.path.dirname(redirect.file), exist_ok=True)
      with open(redirect.file, "w") as f:
        subprocess.run([path] + arguments, stdout=f, text=True)
    elif redirect.type == RedirectionType.STDERR:
      os.makedirs(os.path.dirname(redirect.file), exist_ok=True)
      with open(redirect.file, "w") as f:
        subprocess.run([path] + arguments, stderr=f, text=True)
    else:
      subprocess.run([path] + arguments, text=True)
  else:
    execute_not_found(command, redirect)


def execute_not_found(command: str, redirect: Redirect) -> None:
  output = f"{command}: not found\n"
  handle_output(output, redirect)