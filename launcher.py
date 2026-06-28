#!/usr/bin/env python3
"""
Interactive tmux + Claude session launcher.
Run this to interactively start a new or resume a tmux session,
then optionally launch Claude with new or resume options.
"""

import subprocess
import sys
import secrets
from pathlib import Path

def run_cmd(cmd, shell=False):
    """Execute shell command, return stdout as string."""
    try:
        result = subprocess.run(
            cmd if shell else cmd.split(),
            capture_output=True,
            text=True,
            shell=shell
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        print(f"Error running command: {e}")
        return "", 1

def list_tmux_sessions():
    """List all tmux sessions with activity info."""
    cmd = "tmux ls -F '#{session_activity} | ID: #{session_id} | Name: #{session_name} | Created: #{t:session_created}' | sort -rg"
    output, code = run_cmd(cmd, shell=True)
    if code == 0 and output:
        return output.split('\n')
    return []

def step_1_tmux():
    """Step 1: Ask new or resume tmux session."""
    print("\n=== TMUX SESSION ===")
    print("1) New tmux session")
    print("2) Resume existing session")
    choice = input("Pick 1 or 2: ").strip()

    if choice == "1":
        # 1a: New session
        hex_code = secrets.token_hex(3)
        session_name = f"claude-{hex_code}"
        print(f"\n✓ Creating new session: {session_name}")
        run_cmd(f"tmux new-session -d -s {session_name}", shell=True)
        run_cmd(f"tmux send-keys -t {session_name} 'clear' Enter", shell=True)
        return session_name

    elif choice == "2":
        # 1b: Resume session
        sessions = list_tmux_sessions()
        if not sessions:
            print("No tmux sessions found.")
            return step_1_tmux()  # Retry

        print("\nAvailable sessions (sorted by recent activity):")
        for i, sess in enumerate(sessions, 1):
            print(f"{i}) {sess}")

        idx = input("\nPick session number: ").strip()
        try:
            selected = sessions[int(idx) - 1]
            # Extract session name (last field after "Name: ")
            session_name = selected.split("| Name: ")[-1].split(" |")[0]
            print(f"\n✓ Resuming session: {session_name}")
            return session_name
        except (ValueError, IndexError):
            print("Invalid choice, try again.")
            return step_1_tmux()
    else:
        print("Invalid choice.")
        return step_1_tmux()

def step_2_claude(session_name):
    """Step 2: Ask new or resume Claude session."""
    print("\n=== CLAUDE SESSION ===")
    print("1) New Claude session (remote-control)")
    print("2) Resume Claude session")
    choice = input("Pick 1 or 2: ").strip()

    if choice == "1":
        print(f"\n✓ Launching Claude (new remote-control)")
        run_cmd(f"tmux send-keys -t {session_name} 'claude remote-control' Enter", shell=True)
    elif choice == "2":
        print(f"\n✓ Launching Claude (resume)")
        run_cmd(f"tmux send-keys -t {session_name} 'claude resume' Enter", shell=True)
    else:
        print("Invalid choice.")
        return step_2_claude(session_name)

    print(f"\n✓ Attaching to tmux session '{session_name}'...")
    run_cmd(f"tmux attach-session -t {session_name}", shell=True)

if __name__ == "__main__":
    try:
        session = step_1_tmux()
        step_2_claude(session)
    except KeyboardInterrupt:
        print("\n\nAborted.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
