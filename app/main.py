from .command_parser import CommandParser
from .redirect_parser import RedirectParser
from .repl import Repl

def main() -> None:
    redirect_parser = RedirectParser()
    command_parser = CommandParser(redirect_parser)
    repl = Repl(command_parser, )
    repl.run()

if __name__ == "__main__":
    main()


