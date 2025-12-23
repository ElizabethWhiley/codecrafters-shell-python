import os

def get_executable_path(command: str) -> str | None:
    paths = os.environ.get("PATH")
    if not paths:
        raise ValueError("PATH environment variable is not set")
    paths = paths.split(":")
    for path_dir in paths:
        joined_path = os.path.join(path_dir, command)
        if os.path.exists(joined_path) and os.access(joined_path, os.X_OK):
            return joined_path
    return None

