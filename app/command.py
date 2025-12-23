from .builtin_commands import is_builtin
from .path_utils import get_executable_path
from .redirect import Redirect
from .executor import execute_builtin, execute_external, execute_not_found


class Command:
    def __init__(self, command: str, arguments: list[str], redirects: Redirect):
        self.command = command
        self.arguments = arguments
        self.redirect = redirects

    def execute(self) -> None:
        if self.command:
            if is_builtin(self.command):
                execute_builtin(self.command, self.arguments, self.redirect)
            elif (path := get_executable_path(self.command)):
                execute_external(self.command, self.arguments, self.redirect)
            else:
                execute_not_found(self.command, self.redirect)







