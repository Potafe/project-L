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
    Returns the last 10 commands from each supported shell history file,
    separated by shell type.
    Supports bash, zsh, Windows CMD, and PowerShell.
    """
    home = os.path.expanduser("~")
    history_sources = {
        "Bash": os.path.join(home, ".bash_history"),
        "Zsh": os.path.join(home, ".zsh_history"),
        "PowerShell": os.path.join(
            home, "AppData", "Roaming", "Microsoft", "Windows", "PowerShell", "PSReadLine", "ConsoleHost_history.txt"
        ),
        "CMD": os.path.join(home, "AppData", "Roaming", "cmd_history.txt"),
    }

    all_histories = {}
    for shell, path in history_sources.items():
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = [line.strip() for line in f if line.strip()]
                    all_histories[shell] = lines[-10:] if lines else ["(No commands found)"]
            except Exception as e:
                all_histories[shell] = [f"(Error reading history: {e})"]
        else:
            all_histories[shell] = ["(No history file found)"]
    return all_histories

def main():
    print("=== Git Context ===")
    git_info = git_history()
    print(f"Current branch: {git_info['branch']}")
    print("Status:\n" + (git_info['status'] or "Clean"))
    print("Diff stat:\n" + (git_info['diff_stat'] or "No changes"))

    print("\n=== Last 10 Terminal Commands by Shell ===")
    histories = terminal_history()
    for shell, commands in histories.items():
        print(f"\n--- {shell} ---")
        for i, cmd in enumerate(commands, 1):
            print(f"{i}: {cmd}")

if __name__ == "__main__":
    typer.run(main)