import os
from .redirect import Redirect, RedirectionType

def handle_output(output: str | None, redirect: Redirect) -> None:
  # For builtin commands: STDOUT redirects go to file, STDERR redirects are ignored (builtins don't have separate stderr)
  if redirect.type == RedirectionType.STDOUT:
    # Write output to redirect.file
    if redirect.file:
      os.makedirs(os.path.dirname(redirect.file), exist_ok=True)
      with open(redirect.file, "w") as f:
        f.write(output or "")
        f.flush()
      return None
    else:
      if output:
        print(output, end="", flush=True)
      return None
  else:
    # STDERR redirects and AUTO: print to stdout (builtins don't have separate stderr to redirect)
    if output:
      print(output, end="", flush=True)
    return None