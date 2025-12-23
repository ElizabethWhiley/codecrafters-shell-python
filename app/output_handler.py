import os
from .redirect import Redirect, RedirectionType

# checks redirect type and routes
# cfor file/stout write to file
# for file/stderr write to file
# for stdout/stderr write to stdout/stderr
# for auto write to stdout/stderr
def handle_output(output: str | None, redirect: Redirect) -> None:
  if redirect.type == RedirectionType.STDOUT or redirect.type == RedirectionType.STDERR:
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
    if output:
      print(output, end="", flush=True)
    return None