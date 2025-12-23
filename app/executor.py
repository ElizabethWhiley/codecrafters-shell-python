import os
import subprocess
from .builtin_commands import builtin_handlers
from .path_utils import get_executable_path
from .redirect import Redirect, RedirectionType

def execute_builtin(command: str, arguments: list[str], redirect: Redirect) -> None:
  output = builtin_handlers[command](arguments)
  if redirect.type == RedirectionType.FILE:
    os.makedirs(os.path.dirname(redirect.file), exist_ok=True)
    with open(redirect.file, "w") as f:
      f.write(output or "")
      f.flush()
  else:
    if output:
      print(output, flush=True)

def execute_external(command: str, arguments: list[str], redirect: Redirect) -> None:
  path = get_executable_path(command)
  if path:
    if redirect.type == RedirectionType.FILE:
      os.makedirs(os.path.dirname(redirect.file), exist_ok=True)
      with open(redirect.file, "w") as f:
        subprocess.run([path] + arguments, stdout=f, text=True)
        f.flush()
    else:
      pid = os.fork()
      if pid == 0:
        os.execv(path, [command] + arguments)
      else:
        os.waitpid(pid, 0)
  else:
    execute_not_found(command, redirect)

def execute_not_found(command: str, redirect: Redirect) -> None:
  output = f"{command}: not found"
  if redirect.type == RedirectionType.FILE:
    os.makedirs(os.path.dirname(redirect.file), exist_ok=True)
    with open(redirect.file, "w") as f:
      f.write(output)
      f.flush()
  else:
    print(output, flush=True)
