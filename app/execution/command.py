import subprocess
from typing import TextIO
from ..utils.path import get_executable_path
from ..models.redirect import Redirect
from ..models.shell_context import ShellContext
from .command_executor import CommandExecutor
from .pipe_executor import PipeExecutor
from .builtin_process import BuiltinProcess


class Command:
    """Represents a shell command with arguments and redirection."""
    def __init__(self, command: str, arguments: list[str], redirects: Redirect):
        self.command = command
        self.arguments = arguments
        self.redirect = redirects
        self.executable_path = get_executable_path(command)
        self._command_executor = CommandExecutor()
        self._pipe_executor = PipeExecutor()

    def execute(self, context: ShellContext | None = None) -> None:
        """Execute this command with output redirection."""
        self._command_executor.execute(self, context)

    def execute_with_pipe(
        self,
        stdin: TextIO | None = None,
        stdout: TextIO | int | None = None,
        stderr: TextIO | int | None = None,
        context: ShellContext | None = None
    ) -> BuiltinProcess | subprocess.Popen:
        """Execute this command in a pipeline context."""
        return self._pipe_executor.execute(self, stdin, stdout, stderr, context)
