from .parsing.shell_parser import ShellLineParser
from .parsing.redirect_parser import RedirectParser
from .ui.repl import Repl

def main() -> None:
    redirect_parser = RedirectParser()
    command_parser = ShellLineParser(redirect_parser)
    repl = Repl(command_parser)
    repl.run()

if __name__ == "__main__":
    main()
