import os
from .redirect import Redirect, RedirectionType

def handle_output(output: str | None, redirect: Redirect) -> None:
  # For builtin commands: STDOUT redirects go to file, STDERR redirects are ignored (builtins don't have separate stderr)
  if redirect.type == RedirectionType.STDOUT:
    # Write output to redirect.file
    if redirect.file:
      os.makedirs(os.path.dirname(redirect.file), exist_ok=True)
      with open(redirect.file, redirect.mode.value) as f:
        f.write(output or "")
        f.flush()
      return None
    else:
      if output:
        print(output, end="", flush=True)
      return None
  elif redirect.type == RedirectionType.STDERR:
    # STDERR redirect with builtin: create empty file (builtins don't have stderr), but output still goes to stdout
    if redirect.file:
      os.makedirs(os.path.dirname(redirect.file), exist_ok=True)
      with open(redirect.file, redirect.mode.value) as f:
        f.write("")  # Create empty file
        f.flush()
    # Print output to stdout (builtins don't have separate stderr to redirect)
    if output:
      print(output, end="", flush=True)
    return None
  else:
    # AUTO: print to stdout
    if output:
      print(output, end="", flush=True)
    return None