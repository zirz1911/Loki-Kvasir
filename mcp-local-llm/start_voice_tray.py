#!/usr/bin/env python3
"""
Auto-start Oracle Voice Tray when Claude Code session starts.
Checks if already running — skips if yes, starts if no.
"""

import subprocess
import requests
import os

VOICE_URL = "http://127.0.0.1:37779/status"
TRAY_DIR = r"D:\oracle-voice-tray"
NODE_PATH = r"C:\Program Files\nodejs"
CARGO_PATH = r"C:\Users\pajipan\.cargo\bin"


def is_running() -> bool:
    try:
        requests.get(VOICE_URL, timeout=2)
        return True
    except Exception:
        return False


def start_tray():
    env = os.environ.copy()
    env["PATH"] = f"{NODE_PATH};{CARGO_PATH};" + env.get("PATH", "")

    subprocess.Popen(
        ["cmd", "/c", "npm run tauri dev"],
        cwd=TRAY_DIR,
        env=env,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )


if __name__ == "__main__":
    if not is_running():
        start_tray()
