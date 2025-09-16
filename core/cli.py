import os
import subprocess

import typer
from typing_extensions import Annotated

# context → git status, git diff --stat, current branch.
# Terminal history → last 10 commands (via history).

def git_history():
    branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
    status = subprocess.check_output(["git", "status", "--short"], text=True).strip()
    diff_stat = subprocess.check_output(["git", "diff", "--stat"], text=True).strip()
    return {
        "branch": branch,
        "status": status,
        "diff_stat": diff_stat
    }

def terminal_history():
    """
    Returns the last 10 commands from the user's shell history.
    Supports bash and zsh on Windows (e.g., WSL, Git Bash, or Cygwin).
    Falls back to searching for .bash_history or .zsh_history in the user's home directory.
    """
    home = os.path.expanduser("~")
    history_files = [".bash_history", ".zsh_history"]
    history_path = None

    for fname in history_files:
        candidate = os.path.join(home, fname)
        if os.path.exists(candidate):
            history_path = candidate
            break

    if not history_path:
        return ["No shell history file found."]

    try:
        with open(history_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            return [line.strip() for line in lines[-10:] if line.strip()]
    except Exception as e:
        return [f"Error reading history: {e}"]

def main():
    print("=== Git Context ===")
    git_info = git_history()
    print(f"Current branch: {git_info['branch']}")
    print("Status:\n" + (git_info['status'] or "Clean"))
    print("Diff stat:\n" + (git_info['diff_stat'] or "No changes"))

    print("\n=== Last 10 Terminal Commands ===")
    history = terminal_history()
    for i, cmd in enumerate(history, 1):
        print(f"{i}: {cmd}")

if __name__ == "__main__":
    typer.run(main)