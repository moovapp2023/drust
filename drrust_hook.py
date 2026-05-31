#!/usr/bin/env python3
"""
D•RUST Claude Code hook — UserPromptSubmit.
Triggers a move if:
  - Prompt is exactly "drust" / "d•rust" / "d.rust", OR
  - It's been >15 min since the last trigger
"""

import json
import sys
import os
import time
import urllib.request

STATE_FILE          = os.path.expanduser('~/.drrust_state')
TIMER_INTERVAL_SECS = 30 * 60


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {'last_trigger': 0}  # 0 = never → first prompt always fires


def save_state(state):
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
    except Exception:
        pass


def trigger_daemon():
    try:
        req = urllib.request.Request('http://127.0.0.1:7433/trigger', data=b'', method='POST')
        urllib.request.urlopen(req, timeout=0.5)
    except Exception:
        pass


def main():
    data   = json.loads(sys.stdin.read())
    prompt = data.get('prompt', '').strip().lower()
    now    = time.time()
    state  = load_state()

    keyword = 'drust' in prompt
    timer_due = (now - state.get('last_trigger', 0)) > TIMER_INTERVAL_SECS

    if keyword or timer_due:
        state['last_trigger'] = now
        trigger_daemon()

    save_state(state)
    sys.stdout.write(json.dumps({'decision': 'allow'}) + '\n')
    sys.stdout.flush()


if __name__ == '__main__':
    main()
