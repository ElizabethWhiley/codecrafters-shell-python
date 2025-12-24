import os
from ..ui.history import History

class ShellContext:
    """Shell execution context containing shared state."""

    def __init__(self, history: History):
        self.history = history
        self.working_dir = os.getcwd()
        self.env_vars = os.environ.copy()
