import os
import subprocess
from ..builtins.handlers import is_builtin, builtin_handlers
from ..utils.path import get_executable_path
from ..models.redirect import Redirect, RedirectionType
from ..utils.output import handle_output
from .builtin_process import BuiltinProcess


class Command:
    """Represents a shell command with arguments and redirection."""
    def __init__(self, command: str, arguments: list[str], redirects: Redirect):
        self.command = command
        self.arguments = arguments
        self.redirect = redirects
        self.executable_path = get_executable_path(command)

    def execute(self, context=None) -> None:
        if self.command:
            if is_builtin(self.command):
                self._execute_builtin(context=context)
            elif self.executable_path:
                self._execute_external()
            else:
                self._execute_not_found()

    def _execute_builtin(self, context=None) -> None:
        output = builtin_handlers[self.command](self.arguments, context=context)
        handle_output(output, self.redirect)

    def _execute_external(self) -> None:
        if self.redirect.type in (RedirectionType.STDOUT, RedirectionType.STDERR):
            self._execute_with_file_redirect()
        else:
            subprocess.run(
                [self.command] + self.arguments,
                executable=self.executable_path,
                text=True,
                check=False
            )

    def _execute_not_found(self) -> None:
        output = f"{self.command}: not found\n"
        handle_output(output, self.redirect)

    def _execute_with_file_redirect(self) -> None:
        os.makedirs(os.path.dirname(self.redirect.file), exist_ok=True)
        with open(self.redirect.file, self.redirect.mode.value, encoding="utf-8") as file:
            if self.redirect.type == RedirectionType.STDOUT:
                subprocess.run(
                    [self.command] + self.arguments,
                    executable=self.executable_path,
                    stdout=file,
                    text=True,
                    check=False
                )
            elif self.redirect.type == RedirectionType.STDERR:
                subprocess.run(
                    [self.command] + self.arguments,
                    executable=self.executable_path,
                    stderr=file,
                    text=True,
                    check=False
                )

    def execute_with_pipe(self, stdin=None, stdout=None, stderr=None, context=None):
        if is_builtin(self.command):
            stdin_input = stdin if stdin and hasattr(stdin, 'read') else None

            output = builtin_handlers[self.command](
                self.arguments,
                stdin=stdin_input,
                context=context
            )
            output = output or ""

            # If stdout is None (last command), print to terminal
            if stdout is None:
                print(output, end="", flush=True)
                return BuiltinProcess(output, needs_pipe=False)
            # If stdout is PIPE, create pipe for next command
            if stdout == subprocess.PIPE:
                return BuiltinProcess(output, needs_pipe=True)
            # Otherwise, write to provided stdout
            stdout.write(output)
            stdout.flush()
            return BuiltinProcess(output, needs_pipe=False)
        # External command - use subprocess.Popen
        if not self.executable_path:
            raise FileNotFoundError(f"{self.command}: not found")
        return subprocess.Popen(
            [self.command] + self.arguments,
            executable=self.executable_path,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            text=True
        )
