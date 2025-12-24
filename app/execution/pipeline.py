from .command import Command
import subprocess

class Pipeline:
  def __init__(self, commands: list[Command]):
    self.commands = commands

  def execute(self, context=None) -> None:
    processes = []
    previous_process = None
    for i, command in enumerate(self.commands):
      if i == 0:
        process = command.execute_with_pipe(stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, context=context)
        processes.append(process)
        previous_process = process
      elif i == len(self.commands) - 1:
        process = command.execute_with_pipe(stdin=previous_process.stdout, stdout=None, stderr=None, context=context)
        processes.append(process)
        previous_process = process
      else:
        process = command.execute_with_pipe(stdin=previous_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, context=context)
        processes.append(process)
        previous_process = process

    for process in processes:
        process.wait()

