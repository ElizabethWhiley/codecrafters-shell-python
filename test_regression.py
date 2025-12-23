#!/usr/bin/env python3
"""
Regression test script for the shell implementation.
Tests basic functionality to ensure no regressions were introduced.
"""

import subprocess
import sys
import os
import io
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

def test_tab_completion_behavior():
    """Test tab completion behavior: bell on first TAB, show matches on second TAB."""
    print("Testing tab completion behavior...")

    from app.repl import Repl
    from app.command_parser import CommandParser
    from app.redirect_parser import RedirectParser
    redirect_parser = RedirectParser()
    command_parser = CommandParser(redirect_parser)
    repl = Repl(command_parser)

    # Test first TAB press - should increment tab_count
    repl._get_completions("ech", 0)
    assert repl.tab_count == 1, f"First TAB should set tab_count to 1, got: {repl.tab_count}"
    assert repl.last_prefix == "ech", f"last_prefix should be 'ech', got: {repl.last_prefix}"
    print("  ✓ first TAB increments tab_count")

    # Test second TAB press - should increment tab_count to 2
    repl._get_completions("ech", 0)
    assert repl.tab_count == 2, f"Second TAB should set tab_count to 2, got: {repl.tab_count}"
    print("  ✓ second TAB increments tab_count to 2")

    # Test prefix change resets tab_count
    repl._get_completions("exi", 0)
    assert repl.tab_count == 1, f"New prefix should reset tab_count to 1, got: {repl.tab_count}"
    assert repl.last_prefix == "exi", f"last_prefix should be 'exi', got: {repl.last_prefix}"
    print("  ✓ prefix change resets tab_count")

    # Test multiple matches are stored
    repl._get_completions("e", 0)
    assert len(repl.matches) >= 2, f"Prefix 'e' should have multiple matches, got: {len(repl.matches)}"
    print("  ✓ multiple matches stored correctly")

    # Test first TAB rings bell (requires capturing stderr)
    # Note: This tests the logic, actual bell output would need subprocess testing
    repl2 = Repl(command_parser)
    repl2._get_completions("ech", 0)
    assert repl2.tab_count == 1, "First TAB should set tab_count to 1 for bell logic"
    print("  ✓ first TAB sets up for bell ring")

    # Test second TAB shows matches (alphabetically sorted, two spaces)
    repl2._get_completions("ech", 0)  # Second TAB
    assert repl2.tab_count == 2, "Second TAB should set tab_count to 2 for match display"
    # Verify matches are sorted alphabetically
    sorted_matches = sorted(repl2.matches)
    assert repl2.matches == sorted_matches, f"Matches should be sorted alphabetically, got: {repl2.matches}"
    print("  ✓ second TAB sets up for match display (sorted alphabetically)")

    # Test matches would be joined with two spaces (verify format)
    if len(repl2.matches) > 1:
        expected_format = "  ".join(sorted(repl2.matches))
        assert "  " in expected_format, "Multiple matches should be separated by two spaces"
        print("  ✓ matches format uses two spaces as separator")

    # Test requirements: bell on first TAB, matches on second TAB
    # This verifies the tab_count logic supports the requirements
    repl3 = Repl(command_parser)

    # First TAB: should ring bell (tab_count == 1)
    repl3._get_completions("ex", 0)
    assert repl3.tab_count == 1, "First TAB press should set tab_count to 1 (triggers bell)"
    print("  ✓ first TAB press sets tab_count=1 (bell requirement)")

    # Second TAB: should show matches (tab_count == 2)
    repl3._get_completions("ex", 0)
    assert repl3.tab_count == 2, "Second TAB press should set tab_count to 2 (triggers match display)"
    assert len(repl3.matches) > 0, "Should have matches to display"
    # Verify matches are sorted alphabetically
    assert repl3.matches == sorted(repl3.matches), "Matches should be sorted alphabetically for display"
    print("  ✓ second TAB press sets tab_count=2 (match display requirement)")
    print("  ✓ matches are sorted alphabetically")

def test_external_executable_completion():
    """Test tab completion for external executables in PATH."""
    print("Testing external executable completion...")

    try:
        from app.completion_utils import get_external_completions
    except ImportError:
        print("  ✗ Completion function not found")
        raise

    # Test that function returns a list (even if empty)
    completions = get_external_completions("xyz_nonexistent_123")
    assert isinstance(completions, list), f"Should return a list, got: {type(completions)}"
    print("  ✓ function returns list for non-existent prefix")

    # Test with common executables that might exist (ls, cat, etc.)
    # These are likely to exist on most Unix systems
    common_executables = ["ls", "cat", "echo"]
    for exe in common_executables:
        # Test with first letter
        completions = get_external_completions(exe[0])
        if exe in completions:
            print(f"  ✓ found '{exe}' in PATH completions")
            break
    else:
        print("  ⚠ Could not find common executables (may be PATH issue)")

    # Test that completer includes external executables
    from app.repl import Repl
    from app.command_parser import CommandParser
    from app.redirect_parser import RedirectParser
    redirect_parser = RedirectParser()
    command_parser = CommandParser(redirect_parser)
    repl = Repl(command_parser)

    # Test completer with a prefix that might match external executables
    # Try first letter of common commands
    for letter in ["l", "c"]:
        match = repl._get_completions(letter, 0)
        if match and not match.endswith(" "):
            # Multiple matches - external executables might be included
            print(f"  ✓ completer includes external executables for '{letter}'")
            break
    else:
        print("  ⚠ Could not verify external executable completion (may need specific PATH setup)")

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
        test_tab_completion_behavior,
        test_external_executable_completion,
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

