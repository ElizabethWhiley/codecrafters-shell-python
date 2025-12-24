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
          is_first = (i == 0)
          is_last = (i == len(self.commands) - 1)

          stdin = None if is_first else previous_process.stdout
          stdout = None if is_last else subprocess.PIPE
          stderr = None if is_last else subprocess.PIPE

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
