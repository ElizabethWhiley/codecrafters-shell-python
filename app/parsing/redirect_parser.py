from ..models.redirect import Redirect, RedirectionType, FileMode

class RedirectParser:
    """Parses redirection operators from command arguments."""
    def __init__(self):
        self._redirect_map = {
            ">": (RedirectionType.STDOUT, FileMode.WRITE),
            "1>": (RedirectionType.STDOUT, FileMode.WRITE),
            "2>": (RedirectionType.STDERR, FileMode.WRITE),
            ">>": (RedirectionType.STDOUT, FileMode.APPEND),
            "1>>": (RedirectionType.STDOUT, FileMode.APPEND),
            "2>>": (RedirectionType.STDERR, FileMode.APPEND),
            "&>": (RedirectionType.AUTO, FileMode.WRITE),
            "&>>": (RedirectionType.AUTO, FileMode.APPEND),
        }

    def parse_redirects(self, arguments: list[str]) -> tuple[Redirect, list[str]]:
        for i, arg in enumerate(arguments):
            redirect_type, mode = self._parse_redirect_type(arg)  # Unpack the tuple
            if redirect_type != RedirectionType.AUTO:  # Found a redirect operator
                if i + 1 >= len(arguments):
                    return Redirect(RedirectionType.AUTO, FileMode.WRITE, None), arguments
                # Return cleaned arguments (everything before the operator)
                return Redirect(redirect_type, mode, arguments[i + 1]), arguments[:i]
        # No redirect found
        return Redirect(RedirectionType.AUTO, FileMode.WRITE, None), arguments

    def _parse_redirect_type(self, argument: str) -> tuple[RedirectionType, FileMode]:
        return self._redirect_map.get(argument, (RedirectionType.AUTO, FileMode.WRITE))
