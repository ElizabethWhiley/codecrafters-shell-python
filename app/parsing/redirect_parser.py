from ..models.redirect import Redirect, RedirectionType, RedirectMode

class RedirectParser:
    """Parses redirection operators from command arguments."""
    def __init__(self):
        self._redirect_map = {
            ">": (RedirectionType.STDOUT, RedirectMode.WRITE),
            "1>": (RedirectionType.STDOUT, RedirectMode.WRITE),
            "2>": (RedirectionType.STDERR, RedirectMode.WRITE),
            ">>": (RedirectionType.STDOUT, RedirectMode.APPEND),
            "1>>": (RedirectionType.STDOUT, RedirectMode.APPEND),
            "2>>": (RedirectionType.STDERR, RedirectMode.APPEND),
            "&>": (RedirectionType.AUTO, RedirectMode.WRITE),
            "&>>": (RedirectionType.AUTO, RedirectMode.APPEND),
        }

    def parse_redirects(self, arguments: list[str]) -> tuple[Redirect, list[str]]:
        for i, arg in enumerate(arguments):
            redirect_type, mode = self._parse_redirect_type(arg)  # Unpack the tuple
            if redirect_type != RedirectionType.AUTO:  # Found a redirect operator
                if i + 1 >= len(arguments):
                    return Redirect(RedirectionType.AUTO, RedirectMode.WRITE, None), arguments
                # Return cleaned arguments (everything before the operator)
                return Redirect(redirect_type, mode, arguments[i + 1]), arguments[:i]
        # No redirect found
        return Redirect(RedirectionType.AUTO, RedirectMode.WRITE, None), arguments

    def _parse_redirect_type(self, argument: str) -> tuple[RedirectionType, RedirectMode]:
        return self._redirect_map.get(argument, (RedirectionType.AUTO, RedirectMode.WRITE))
