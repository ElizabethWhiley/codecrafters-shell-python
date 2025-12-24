import subprocess
from typing import TextIO, TYPE_CHECKING
from ..builtins.handlers import is_builtin, builtin_handlers
from ..models.shell_context import ShellContext
from ..utils.subprocess_utils import build_subprocess_kwargs
from .builtin_process import BuiltinProcess

if TYPE_CHECKING:
    from .command import Command


class PipeExecutor:
    """Executes a command in a pipeline context."""

    def execute(
        self,
        command: "Command",
        stdin: TextIO | None = None,
        stdout: TextIO | int | None = None,
        stderr: TextIO | int | None = None,
        context: ShellContext | None = None
    ) -> BuiltinProcess | subprocess.Popen:
        """Execute a command with pipe I/O redirection."""
        if is_builtin(command.command):
            return self._execute_builtin_with_pipe(command, stdin, stdout, stderr, context)
        return self._execute_external_with_pipe(command, stdin, stdout, stderr)

    def _execute_builtin_with_pipe(
        self,
        command: "Command",
        stdin: TextIO | None,
        stdout: TextIO | int | None,
        stderr: TextIO | None,  # pylint: disable=unused-argument
        context: ShellContext | None
    ) -> BuiltinProcess:
        """Execute a builtin command in a pipeline."""
        stdin_input = stdin if stdin and hasattr(stdin, "read") else None

        output = builtin_handlers[command.command](
            command.arguments,
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

    def _execute_external_with_pipe(
        self,
        command: "Command",
        stdin: TextIO | None,
        stdout: TextIO | int | None,
        stderr: TextIO | int | None
    ) -> subprocess.Popen:
        """Execute an external command in a pipeline."""
        if not command.executable_path:
            raise FileNotFoundError(f"{command.command}: not found")
        return subprocess.Popen(
            **build_subprocess_kwargs(command, stdin=stdin, stdout=stdout, stderr=stderr)
        )
