#!/usr/bin/env python3
"""
Run this once to produce install.py — the single file you share with your friend.
Usage: python3 build_installer.py
"""
import base64, json, os

HERE = os.path.dirname(os.path.abspath(__file__))

FILES = [
    "drrust_daemon.py",
    "drrust_hook.py",
    "drrust_widget.html",
    "widget.css",
    "moves_db.js",
    "version.txt",
]

INSTALL_DIR = "~/.drrust"

embedded = {}
for name in FILES:
    path = os.path.join(HERE, name)
    with open(path, "rb") as f:
        embedded[name] = base64.b64encode(f.read()).decode()

installer = f'''\
#!/usr/bin/env python3
import base64, os, json, subprocess, sys

FILES = {json.dumps(embedded, indent=2)}

INSTALL_DIR = os.path.expanduser("{INSTALL_DIR}")
os.makedirs(INSTALL_DIR, exist_ok=True)

print("Writing files to", INSTALL_DIR)
for name, b64 in FILES.items():
    dest = os.path.join(INSTALL_DIR, name)
    with open(dest, "wb") as f:
        f.write(base64.b64decode(b64))
    if name.endswith(".py"):
        os.chmod(dest, 0o755)

print("Installing pywebview...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "pywebview", "-q"])

settings_path = os.path.expanduser("~/.claude/settings.json")
try:
    with open(settings_path) as f:
        settings = json.load(f)
except Exception:
    settings = {{}}

hook_cmd = f"python3 {{os.path.join(INSTALL_DIR, 'drrust_hook.py')}}"
new_hook = {{"type": "command", "command": hook_cmd}}

hooks = settings.setdefault("hooks", {{}})
submit = hooks.setdefault("UserPromptSubmit", [])
if not submit:
    submit.append({{"matcher": "", "hooks": []}})
entry = submit[0]
existing = entry.setdefault("hooks", [])
if not any(h.get("command") == hook_cmd for h in existing):
    existing.append(new_hook)

with open(settings_path, "w") as f:
    json.dump(settings, f, indent=2)

print()
print("Done! Start the daemon with:")
print(f"  python3 {{os.path.join(INSTALL_DIR, 'drrust_daemon.py')}}")
'''

out = os.path.join(HERE, "install.py")
with open(out, "w") as f:
    f.write(installer)
os.chmod(out, 0o755)
print(f"Built: {out}")
print("Share install.py with your friend — they just run: python3 install.py")
