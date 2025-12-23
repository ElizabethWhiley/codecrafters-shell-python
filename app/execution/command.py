import os
import subprocess
from ..builtins.handlers import is_builtin, builtin_handlers
from ..utils.path import get_executable_path
from ..models.redirect import Redirect, RedirectionType
from ..utils.output import handle_output


class Command:
    def __init__(self, command: str, arguments: list[str], redirects: Redirect):
        self.command = command
        self.arguments = arguments
        self.redirect = redirects
        self.executable_path = get_executable_path(command)

    def execute(self) -> None:
        if self.command:
            if is_builtin(self.command):
                self._execute_builtin()
            elif (self.executable_path):
                self._execute_external()
            else:
                self._execute_not_found()

    def _execute_builtin(self) -> None:
        output = builtin_handlers[self.command](self.arguments)
        handle_output(output, self.redirect)

    def _execute_external(self) -> None:
        if self.redirect.type == RedirectionType.STDOUT or self.redirect.type == RedirectionType.STDERR:
            self._execute_with_file_redirect()
        else:
            subprocess.run([self.command] + self.arguments, executable=self.executable_path, text=True)

    def _execute_not_found(self) -> None:
        output = f"{self.command}: not found\n"
        handle_output(output, self.redirect)

    def _execute_with_file_redirect(self) -> None:
        os.makedirs(os.path.dirname(self.redirect.file), exist_ok=True)
        with open(self.redirect.file, self.redirect.mode.value) as f:
            if self.redirect.type == RedirectionType.STDOUT:
                subprocess.run([self.command] + self.arguments, executable=self.executable_path, stdout=f, text=True)
            elif self.redirect.type == RedirectionType.STDERR:
                subprocess.run([self.command] + self.arguments, executable=self.executable_path, stderr=f, text=True)

    def execute_with_pipe(self, stdin=None, stdout=None, stderr=None) -> subprocess.Popen:
        return subprocess.Popen([self.command] + self.arguments, executable=self.executable_path, stdin=stdin, stdout=stdout, stderr=stderr, text=True)

