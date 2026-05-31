# D•RUST

Move widget for Claude Code. Pops up a set of moves while you're working — every 30 minutes or whenever you type `drust` in a prompt.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/moovapp2023/drrust/main/install.py | python3
```

That's it. The installer:
- Copies files to `~/.drrust/`
- Installs `pywebview`
- Wires up the Claude Code hook automatically

## Start the daemon

Run this once before (or alongside) Claude Code:

```bash
python3 ~/.drrust/drrust_daemon.py
```

The daemon auto-updates on every startup — you'll always be on the latest version.

## Updating (for contributors)

1. Edit source files
2. Bump `version.txt`
3. Run `python3 build_installer.py` to regenerate `install.py`
4. Push — existing users get the update automatically next time they start the daemon
