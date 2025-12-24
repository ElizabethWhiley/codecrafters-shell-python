[![progress-banner](https://backend.codecrafters.io/progress/shell/44496bf5-d653-41b9-ac66-3237428da9a5)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

This is a Python solution to the
["Build Your Own Shell" Challenge](https://app.codecrafters.io/courses/shell/overview).

A POSIX-compliant shell implementation that interprets shell commands, runs external programs,
and handles builtin commands like `cd`, `pwd`, `echo`, `history`, and more. Features include
command parsing, pipelines, redirection, command history, and tab completion.

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to try the challenge.

## Quick Start

### Running Locally

1. Ensure you have `uv` installed locally
2. Run `./your_program.sh` to start the shell
3. The entry point is `app/main.py`

### Submitting to CodeCrafters

```sh
git commit -am "your commit message"
git push origin master
```

Test output will be streamed to your terminal.

## Why did I complete this challenge?

This challenge teaches you:

- **REPLs (Read-Eval-Print Loops)**: How interactive shells work
- **Command Parsing**: Tokenizing and parsing shell command lines
- **Process Management**: Using `subprocess` to run external programs
- **Pipes & Redirection**: Handling I/O redirection and command chaining
- **Builtin Commands**: Implementing shell-native commands vs external programs
- **State Management**: Managing shell context (working directory, environment, history)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Input                          │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │   REPL (UI)     │  ← Command history, tab completion
                    │  app/ui/repl.py │
                    └────────┬───────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Shell Parser   │  ← Parse command line
                    │app/parsing/    │     - Extract commands
                    │shell_parser.py │     - Detect pipes (|)
                    └────────┬───────┘     - Extract redirects (> >> 2>)
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
        ┌───────────────┐        ┌───────────────┐
        │   Command     │        │   Pipeline    │ → Orchestrates multiple commands
        │  (single cmd) │       │  (cmd1 | cmd2) │ → Connects commands with pipes
        └───────┬───────┘        └───────┬───────┘
                │                        │
                │                        │
                ▼                        ▼
        ┌──────────────┐        ┌──────────────┐
        │   Command    │        │  Pipe        │
        │   Executor   │        │  Executor    │
        │ (standalone) │        │ (each cmd)   │
        └──────┬───────┘        └───────┬──────┘
               │                        │
               │                        │
               └────────────┬───────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼
    ┌──────────────┐              ┌──────────────┐
    │   Builtin    │              │   External   │
    │   Handlers   │              │  subprocess  │
    │app/builtins/ │              │    Popen     │
    └──────────────┘              └──────────────┘
```

### Key Components

- **`app/ui/repl.py`**: Main REPL loop, handles user input and command history
- **`app/parsing/`**: Command line parsing (shell_parser, redirect_parser)
- **`app/execution/`**: Command execution
  - `command.py`: Command data model
  - `command_executor.py`: Standalone command execution with redirects
  - `pipe_executor.py`: Pipeline execution
  - `pipeline.py`: Orchestrates multi-command pipelines
- **`app/builtins/handlers.py`**: Builtin command implementations
- **`app/models/`**: Data models (Redirect with FileMode enum, ShellContext)
- **`app/utils/`**: Utilities (path resolution, output handling, completion, subprocess argument building)

## Tricky parts

### 1. Output redirection

Handling `>`, `>>`, and `2>`, `2>>` operators required careful parsing and file I/O management:

- **Parsing**: Extracting redirect operators from command arguments without breaking argument parsing
- **File handling**: Creating parent directories, handling permission errors gracefully
- **Stream management**: Properly redirecting stdout/stderr to files

**What I learnt**: Redirects need to be parsed separately from arguments, otherwise you end up with redirect operators as command arguments. The redirect information is then applied during execution, not during parsing.

### 2. Pipes

Pipelines (`cmd1 | cmd2 | cmd3`) were one of the complex features:

- **Builtin vs External**: Builtin commands return strings, external commands use `subprocess.Popen`
- **I/O chaining**: Each command's stdout becomes the next command's stdin
- **Process management**: Tracking all processes in a pipeline and waiting for completion
- **BuiltinProcess wrapper**: Created a `BuiltinProcess` class to unify builtin and external command handling in pipelines

**What I learnt**: Builtin commands execute synchronously and return strings, while external commands are asynchronous `subprocess.Popen` objects. To make them work together in pipelines, I needed a wrapper class (`BuiltinProcess`) that mimics the interface of a process object so the pipeline can handle both types uniformly.

## Design decisions

### 1. Single responsibility principle (SRP) refactor

The `Command` class initially handled both data representation and execution. This was refactored into:

- **`Command`**: Pure data class (command name, arguments, redirects)
- **`CommandExecutor`**: Handles standalone execution with redirects
- **`PipeExecutor`**: Handles execution within pipelines

This separation makes the code more testable and maintainable.

### 2. Shell context management

Created a `ShellContext` class to manage shared shell state:

- **History**: Command history using Python's `readline` module
- **Working directory**: Current directory (updated by `cd`)
- **Environment variables**: Shell environment state

This centralised state management made it easier to pass context between components.

### 3. Graceful error handling

I tried to get the shell not to crash, even on errors. I wanted it to be resilient and continue running even when individual commands fail.

- **File operations**: Try/except blocks around all file I/O with error messages to stderr
- **Command not found**: Prints error message instead of raising exceptions
- **Permission errors**: Handles file permission issues gracefully

### 4. Builtin vs External Command Handling

Clear separation between builtin and external commands:

- **Builtin commands**: Implemented as Python functions, return strings
- **External commands**: Executed via `subprocess`, return process objects
- **Unified interface**: Both work in pipelines and standalone execution

### 5. Code quality refactoring

Recent improvements to reduce duplication and improve maintainability:

- **Shared subprocess utilities**: Extracted `build_subprocess_kwargs()` to `app/utils/subprocess_utils.py` to eliminate duplication between `CommandExecutor` and `PipeExecutor`
- **Magic values eliminated**: Extracted constants for home directory symbol (`~`), history flags (`-r`, `-w`, `-a`), and file modes
- **Better naming**: Renamed `RedirectMode` to `FileMode` to better reflect its general-purpose use beyond just redirection

## Code quality

- **Linter**: Pylint configured and passing (see `pylintrc`) - enforces naming conventions, complexity limits, and design best practices
- **Type hints**: Added type annotations throughout
- **DRY principles**: Shared utilities eliminate code duplication (e.g., `subprocess_utils.py`)
- **Constants over magic values**: All magic strings/numbers extracted to named constants
- **Consistent style**: Standardised indentation, naming conventions, error handling patterns

## Testing

No local test suite is included. CodeCrafters provides a comprehensive test suite that validates your code and every section, preventing you from submitting code that doesn't pass all tests or introduces regressions. Including:

- All builtin commands
- External command execution
- Pipelines and redirection
- Edge cases and error handling

I added static analysis using Pylint to catch code quality issues before submission.
