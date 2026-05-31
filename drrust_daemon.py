#!/usr/bin/env python3
"""
D•RUST daemon — widget window.
Listens on port 7433: POST /trigger shows widget.
"""

import webview
import threading
import os
import sys
import subprocess
import tempfile
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

VERSION_URL = "https://raw.githubusercontent.com/moovapp2023/drust/main/version.txt"
INSTALL_URL = "https://raw.githubusercontent.com/moovapp2023/drust/main/install.py"


def check_for_updates():
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        local_ver_path = os.path.join(here, "version.txt")
        remote = urllib.request.urlopen(VERSION_URL, timeout=3).read().decode().strip()
        local = open(local_ver_path).read().strip() if os.path.exists(local_ver_path) else "0.0.0"
        if remote != local:
            data = urllib.request.urlopen(INSTALL_URL, timeout=10).read()
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="wb") as f:
                f.write(data)
                tmp = f.name
            subprocess.run([sys.executable, tmp], check=True)
            os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception:
        pass

widget_window = None

HERE       = os.path.dirname(os.path.abspath(__file__))
WIDGET_HTML = os.path.join(HERE, 'drrust_widget.html')

# Screen geometry — populated in main() before windows are created
_screen_w = 1920
_screen_h = 1080
_widget_x = 1580


class TriggerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/trigger' and widget_window:
            widget_window.show()
            widget_window.evaluate_js('onTrigger()')
        self.send_response(200)
        self.end_headers()

    def log_message(self, *args):
        pass


def start_server():
    HTTPServer(('127.0.0.1', 7433), TriggerHandler).serve_forever()


class WidgetApi:
    def done(self, count):
        if widget_window:
            widget_window.hide()

    def close(self):
        if widget_window:
            widget_window.hide()

    def resize(self, height):
        if widget_window:
            h = max(400, min(int(height), 1000))
            new_y = _screen_h - h - 60
            widget_window.move(_widget_x, new_y)
            widget_window.resize(300, h)

    def collapse(self, height, width=120):
        if widget_window:
            h = max(40, min(int(height), 400))
            w = max(120, min(int(width), 300))
            new_y = _screen_h - h - 60
            widget_window.move(_widget_x, new_y)
            widget_window.resize(w, h)


def get_positions():
    global _screen_w, _screen_h, _widget_x
    try:
        from AppKit import NSScreen
        f = NSScreen.mainScreen().frame()
        _screen_w, _screen_h = int(f.size.width), int(f.size.height)
        wx = _screen_w - 320 - 20
        _widget_x = wx
        wy = _screen_h - 640 - 60
        return (wx, wy)
    except Exception:
        return (1600, 300)


def main():
    global widget_window
    check_for_updates()
    threading.Thread(target=start_server, daemon=True).start()

    (wx, wy) = get_positions()
    api = WidgetApi()

    widget_window = webview.create_window(
        'D•RUST', WIDGET_HTML,
        js_api=api,
        width=300, height=620,
        x=wx, y=wy,
        resizable=False, on_top=False,
        frameless=True, hidden=True,
        background_color='#0f0f0f',
    )

    webview.start(http_server=True)


if __name__ == '__main__':
    main()
