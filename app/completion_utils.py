import os
from .builtin_commands import builtin_handlers

def get_builtin_completions(prefix: str) -> list[str]:
    return [command for command in builtin_handlers.keys() if command.startswith(prefix)]


def get_external_completions(prefix: str) -> list[str]:
    completions = []
    paths = (os.environ.get("PATH") or "").split(":")
    for path_dir in paths:
        if os.path.exists(path_dir):
            for file in os.listdir(path_dir):
                if file.startswith(prefix) and os.access(os.path.join(path_dir, file), os.X_OK):
                    completions.append(file)
    return completions