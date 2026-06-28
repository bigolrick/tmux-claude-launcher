# tmux-claude-launcher

Interactive CLI tool for spawning and managing tmux sessions with Claude remote-control or resume workflows.

## Quick Start

Copy and paste this one-liner into your Termius bash prompt:

```bash
sudo sh -c 'python3 /path/to/launcher.py && echo LAUNCHER-OK'
```

Replace `/path/to/launcher.py` with your actual script location.

## What It Does

1. **Tmux Session**: Create a new session (named `claude-<3-byte hex>`) or resume an existing one
2. **Claude Session**: Launch Claude with either:
   - `claude remote-control` (new session)
   - `claude resume` (existing session)
3. **Attach**: Automatically attaches you to the tmux session

## Usage

Run the script and follow the interactive prompts:

```
=== TMUX SESSION ===
1) New tmux session
2) Resume existing session
Pick 1 or 2: 
```

Select your choice, then pick your Claude mode:

```
=== CLAUDE SESSION ===
1) New Claude session (remote-control)
2) Resume Claude session
Pick 1 or 2: 
```

The script will attach you to your tmux session automatically.

## Requirements

- Python 3.6+
- tmux
- Claude CLI (`claude` command in PATH)

## Installation

1. Clone this repo
2. Copy `launcher.py` to your desired location (e.g., `~/bin/` or your server's scripts folder)
3. Make it executable: `chmod +x launcher.py`
4. Run it: `python3 launcher.py`

## Features

- **Session Listing**: Resume prompts show recent sessions (sorted by activity)
- **Random Session Names**: New sessions get unique names to avoid collisions
- **Interactive Flow**: No config files needed; answer simple prompts
- **Mobile-Friendly**: Works great over Termius on iOS

## License

MIT
