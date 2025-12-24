import os
import io

class BuiltinProcess:
    """Wrapper to mimic subprocess.Popen interface for builtin commands."""

    def __init__(self, output: str, needs_pipe: bool = False):
        self.output = output
        self.returncode = 0

        if needs_pipe:
            # Create a real pipe for the next command to read from
            read_fd, write_fd = os.pipe()
            # Write output to the write end and close it
            with os.fdopen(write_fd, 'w') as w:
                w.write(output)
            # Return the read end as stdout
            self.stdout = os.fdopen(read_fd, 'r')
        else:
            # No pipe needed, create StringIO for compatibility
            self.stdout = io.StringIO(output)

    def wait(self) -> int:
        """Wait for process to complete (builtins complete immediately)."""
        return self.returncode
