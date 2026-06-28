#!/usr/bin/env python3
"""
Interactive tmux + Claude session launcher.
Run this to interactively start a new or resume a tmux session,
then optionally launch Claude with new or resume options.
"""

import os
import subprocess
import sys
import secrets


def run_cmd(cmd):
    """Execute shell command, return (stdout, returncode)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        print(f"Error running command: {e}")
        return "", 1


def attach_session(session_name):
    """Replace current process with tmux attach — required for live TTY."""
    os.execvp("tmux", ["tmux", "attach-session", "-t", session_name])


def list_tmux_sessions():
    """Return list of session names sorted by most recent activity."""
    # Use \t as separator — can't appear in tmux session names
    cmd = "tmux ls -F '#{session_activity}\t#{session_name}' | sort -rg"
    output, code = run_cmd(cmd)
    if code != 0 or not output:
        return []
    sessions = []
    for line in output.split('\n'):
        parts = line.split('\t', 1)
        if len(parts) == 2:
            sessions.append(parts[1])
    return sessions


def prompt_choice(prompt, options):
    """Loop until user picks a valid numbered option. Returns 1-based index."""
    while True:
        for i, opt in enumerate(options, 1):
            print(f"{i}) {opt}")
        raw = input(prompt).strip()
        try:
            idx = int(raw)
            if 1 <= idx <= len(options):
                return idx
        except ValueError:
            pass
        print("Invalid choice, try again.")


def step_1_tmux():
    """Step 1: New or resume tmux session. Returns session name."""
    print("\n=== TMUX SESSION ===")
    choice = prompt_choice("Pick 1 (new) or 2 (resume): ", ["New tmux session", "Resume existing session"])

    if choice == 1:
        hex_code = secrets.token_hex(3)
        session_name = f"claude-{hex_code}"
        print(f"\n✓ Creating new session: {session_name}")
        run_cmd(f"tmux new-session -d -s {session_name}")
        run_cmd(f"tmux send-keys -t {session_name} 'clear' Enter")
        return session_name

    # Resume
    while True:
        sessions = list_tmux_sessions()
        if not sessions:
            print("No tmux sessions found. Create one first.")
            inner = prompt_choice("Pick 1 (new) or 2 (retry list): ", ["New tmux session", "Retry"])
            if inner == 1:
                return step_1_tmux()
            continue

        print("\nAvailable sessions (sorted by recent activity):")
        idx = prompt_choice("\nPick session number: ", sessions)
        session_name = sessions[idx - 1]
        print(f"\n✓ Resuming session: {session_name}")
        return session_name


def step_2_claude(session_name):
    """Step 2: Launch Claude in the tmux session, then attach."""
    print("\n=== CLAUDE SESSION ===")
    choice = prompt_choice("Pick 1 (new remote-control) or 2 (resume): ",
                           ["New Claude session (remote-control)", "Resume Claude session"])

    if choice == 1:
        print("\n✓ Launching Claude (new remote-control)")
        run_cmd(f"tmux send-keys -t {session_name} 'claude remote-control' Enter")
    else:
        print("\n✓ Launching Claude (resume)")
        run_cmd(f"tmux send-keys -t {session_name} 'claude resume' Enter")

    print(f"\n✓ Attaching to tmux session '{session_name}'...")
    attach_session(session_name)  # exec — never returns


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
