from .parser import parse_command
from .builtin_commands import builtin_handlers
from .repl import Repl

def main() -> None:
    repl = Repl(builtin_handlers, parse_command)
    repl.run()

if __name__ == "__main__":
    main()


