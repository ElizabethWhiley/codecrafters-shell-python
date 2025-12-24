import subprocess
from .command import Command
from ..models.shell_context import ShellContext

class Pipeline:
    """Executes a sequence of commands connected by pipes."""
    def __init__(self, commands: list[Command]):
        self.commands = commands

    def execute(self, context: ShellContext | None = None) -> None:
        processes = []
        previous_process = None

        for i, command in enumerate(self.commands):
            first_command = i == 0
            last_command = i == len(self.commands) - 1

            stdin = None if first_command else previous_process.stdout
            stdout = None if last_command else subprocess.PIPE
            stderr = None if last_command else subprocess.PIPE

            process = command.execute_with_pipe(
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
                context=context
            )
            processes.append(process)
            previous_process = process

        for process in processes:
            process.wait()
