import subprocess
import sys
from typing import TextIO, TYPE_CHECKING
from ..builtins.handlers import is_builtin, builtin_handlers
from ..models.redirect import RedirectionType
from ..models.shell_context import ShellContext
from ..utils.output import handle_output, _ensure_directory_exists

if TYPE_CHECKING:
    from .command import Command


class CommandExecutor:
    """Executes a command with redirects (standalone execution)."""

    def execute(self, command: "Command", context: ShellContext | None = None) -> None:
        """Execute a command with output redirection."""
        if not command.command:
            return

        if is_builtin(command.command):
            self._execute_builtin(command, context)
        elif command.executable_path:
            self._execute_external(command)
        else:
            self._execute_not_found(command)

    def _execute_builtin(self, command: "Command", context: ShellContext | None = None) -> None:
        """Execute a builtin command."""
        output = builtin_handlers[command.command](command.arguments, context=context)
        handle_output(output, command.redirect)

    def _build_subprocess_kwargs(
        self,
        command: "Command",
        stdout: TextIO | int | None = None,
        stderr: TextIO | int | None = None
    ) -> dict:
        """Build common subprocess arguments for external commands."""
        return {
            "args": [command.command] + command.arguments,
            "executable": command.executable_path,
            "text": True,
            "stdout": stdout,
            "stderr": stderr,
        }

    def _execute_external(self, command: "Command") -> None:
        """Execute an external command."""
        if command.redirect.type in (RedirectionType.STDOUT, RedirectionType.STDERR):
            self._execute_with_file_redirect(command)
        else:
            subprocess.run(**self._build_subprocess_kwargs(command), check=False)

    def _execute_not_found(self, command: "Command") -> None:
        """Handle command not found error."""
        output = f"{command.command}: not found\n"
        handle_output(output, command.redirect)

    def _execute_with_file_redirect(self, command: "Command") -> None:
        """Execute external command with file redirection."""
        try:
            _ensure_directory_exists(command.redirect.file)
            with open(command.redirect.file, command.redirect.mode.value, encoding="utf-8") as file:
                kwargs = self._build_subprocess_kwargs(command)
                if command.redirect.type == RedirectionType.STDOUT:
                    kwargs["stdout"] = file
                elif command.redirect.type == RedirectionType.STDERR:
                    kwargs["stderr"] = file
                subprocess.run(**kwargs, check=False)
        except (PermissionError, OSError) as error:
            sys.stderr.write(f"shell: cannot redirect to '{command.redirect.file}': {error}\n")
            sys.stderr.flush()
