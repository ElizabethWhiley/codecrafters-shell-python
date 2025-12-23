import os
from ..builtins.handlers import builtin_handlers


def get_all_completions(prefix: str) -> list[str]:
    """Get all completions (builtin + external), removing duplicates."""
    builtin_matches = _get_builtin_completions(prefix)
    external_matches = _get_external_completions(prefix)
    all_matches = builtin_matches + external_matches
    # Remove duplicates while preserving order (builtins first)
    return list(dict.fromkeys(all_matches))

def get_completion_result(matches: list[str], current_text: str) -> str | None:
    """Determine what the completer should return based on matches."""
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0] + " "

    prefix = _find_longest_common_prefix(matches)
    return prefix if len(prefix) > len(current_text) else None

def _get_builtin_completions(prefix: str) -> list[str]:
    return [command for command in builtin_handlers.keys() if command.startswith(prefix)]

def _get_external_completions(prefix: str) -> list[str]:
    completions = []
    paths = (os.environ.get("PATH") or "").split(":")
    for path_dir in paths:
        if os.path.exists(path_dir):
            for file in os.listdir(path_dir):
                if file.startswith(prefix) and os.access(os.path.join(path_dir, file), os.X_OK):
                    completions.append(file)
    return completions

def _find_longest_common_prefix(matches: list[str]) -> str:
    if not matches:
        return ""

    prefix = matches[0]
    for match in matches[1:]:
        while not match.startswith(prefix) and prefix:
            prefix = prefix[:-1]
    return prefix
