#!/usr/bin/env python3
"""
Regression test script for the shell implementation.
Tests basic functionality to ensure no regressions were introduced.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_shell_command(command: str) -> tuple[str, int]:
    """Run a command in the shell and return output and exit code."""
    process = subprocess.Popen(
        [sys.executable, "-m", "app.main"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Send command and exit
    input_text = f"{command}\nexit\n"
    stdout, stderr = process.communicate(input=input_text, timeout=5)
    return stdout, process.returncode

def test_builtin_commands():
    """Test basic builtin commands."""
    print("Testing builtin commands...")

    # Test echo
    output, _ = run_shell_command('echo "hello world"')
    assert "hello world" in output, f"Echo failed. Got: {output}"
    print("  ✓ echo")

    # Test pwd
    output, _ = run_shell_command("pwd")
    assert os.getcwd() in output, f"Pwd failed. Got: {output}"
    print("  ✓ pwd")

    # Test type (builtin)
    output, _ = run_shell_command("type echo")
    assert "shell builtin" in output, f"Type echo failed. Got: {output}"
    print("  ✓ type (builtin)")

def test_redirection():
    """Test output redirection."""
    print("Testing redirection...")

    test_file = "/tmp/test_redirect.txt"

    # Test stdout redirection
    output, _ = run_shell_command(f'echo "test" > {test_file}')
    if os.path.exists(test_file):
        with open(test_file, "r") as f:
            content = f.read()
            assert "test" in content, f"Stdout redirect failed. Got: {content}"
        os.remove(test_file)
        print("  ✓ stdout redirection (>)")

    # Test append
    output, _ = run_shell_command(f'echo "line1" >> {test_file}')
    output, _ = run_shell_command(f'echo "line2" >> {test_file}')
    if os.path.exists(test_file):
        with open(test_file, "r") as f:
            content = f.read()
            assert "line1" in content and "line2" in content, f"Append failed. Got: {content}"
        os.remove(test_file)
        print("  ✓ append redirection (>>)")

def test_command_not_found():
    """Test command not found error."""
    print("Testing error handling...")

    output, _ = run_shell_command("nonexistent_command_xyz")
    assert "not found" in output.lower(), f"Command not found failed. Got: {output}"
    print("  ✓ command not found")

def test_external_commands():
    """Test external command execution."""
    print("Testing external commands...")

    # Test ls (if available)
    output, _ = run_shell_command("ls /tmp 2>&1 | head -5")
    # Just check it doesn't crash
    print("  ✓ external command execution")

def test_tab_completion():
    """Test tab completion for builtin commands."""
    print("Testing tab completion...")

    try:
        from app.completion_utils import get_builtin_completions
    except ImportError:
        print("  ✗ Completion function not found - implement get_builtin_completions() in app/completion.py")
        raise

    # Test "ech" completes to "echo"
    completions = get_builtin_completions("ech")
    assert "echo" in completions, f"'ech' should complete to 'echo', got: {completions}"
    assert len(completions) == 1, f"'ech' should have 1 completion, got: {completions}"
    print("  ✓ 'ech' completes to 'echo'")

    # Test that single matches get trailing space in completer
    # (The completer in repl.py adds a space when there's exactly one match)
    from app.repl import Repl
    from app.command_parser import CommandParser
    from app.redirect_parser import RedirectParser
    redirect_parser = RedirectParser()
    command_parser = CommandParser(redirect_parser)
    repl = Repl(command_parser)
    # Test completer adds space for single match
    single_match = repl._get_completions("ech", 0)
    assert single_match == "echo ", f"Single match should have trailing space, got: '{single_match}'"
    print("  ✓ single match adds trailing space in completer")

    # Test "exi" completes to "exit"
    completions = get_builtin_completions("exi")
    assert "exit" in completions, f"'exi' should complete to 'exit', got: {completions}"
    assert len(completions) == 1, f"'exi' should have 1 completion, got: {completions}"
    print("  ✓ 'exi' completes to 'exit'")

    # Test completer adds space for "exi" -> "exit"
    single_match = repl._get_completions("exi", 0)
    assert single_match == "exit ", f"Single match should have trailing space, got: '{single_match}'"
    print("  ✓ 'exi' completer adds trailing space")

    # Test "e" might match multiple commands
    completions = get_builtin_completions("e")
    assert "echo" in completions, f"'e' should include 'echo', got: {completions}"
    assert "exit" in completions, f"'e' should include 'exit', got: {completions}"
    print("  ✓ 'e' matches multiple commands")

    # Test completer does NOT add space for multiple matches
    first_match = repl._get_completions("e", 0)
    assert first_match in ["echo", "exit"], f"First match should be 'echo' or 'exit', got: '{first_match}'"
    assert not first_match.endswith(" "), f"Multiple matches should NOT have trailing space, got: '{first_match}'"
    print("  ✓ multiple matches do NOT add trailing space")

    # Test no matches
    completions = get_builtin_completions("xyz")
    assert completions == [], f"'xyz' should have no completions, got: {completions}"
    print("  ✓ no matches for invalid prefix")

    # Test empty prefix (might return all or empty - depends on design)
    completions = get_builtin_completions("")
    # Just check it doesn't crash and returns a list
    assert isinstance(completions, list), f"Empty prefix should return a list, got: {type(completions)}"
    print("  ✓ empty prefix handled")

def main():
    """Run all regression tests."""
    print("Running regression tests...\n")

    tests_passed = 0
    tests_failed = 0

    test_functions = [
        test_builtin_commands,
        test_redirection,
        test_command_not_found,
        test_external_commands,
        test_tab_completion,
    ]

    for test_func in test_functions:
        try:
            test_func()
            tests_passed += 1
        except AssertionError as e:
            print(f"  ✗ {test_func.__name__}: {e}")
            tests_failed += 1
        except Exception as e:
            print(f"  ✗ {test_func.__name__}: Unexpected error: {e}")
            tests_failed += 1
        print()

    print(f"Results: {tests_passed} passed, {tests_failed} failed")

    if tests_failed > 0:
        sys.exit(1)
    else:
        print("All tests passed! ✓")
        sys.exit(0)

if __name__ == "__main__":
    main()

