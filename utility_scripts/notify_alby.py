#!/usr/bin/env python3
import os
import sys
import subprocess

def load_env(env_path: str = ".env"):
    """Simple parser to read environment variables from a .env file."""
    # If the default env_path does not exist, check the directory where this script lives
    if not os.path.exists(env_path):
        script_dir_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        if os.path.exists(script_dir_env):
            env_path = script_dir_env

    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip().strip('"').strip("'")

def send_imessage(contact: str, message: str):
    """Uses AppleScript to send an iMessage."""
    escaped_message = message.replace('"', '\\"')
    applescript = f'tell application "Messages" to send "{escaped_message}" to buddy "{contact}"'
    try:
        subprocess.run(["osascript", "-e", applescript], check=True, capture_output=True, text=True)
        print(f"💧 [Daily Drip Notifications] Text message sent: \"{message}\"")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to send iMessage via AppleScript: {e.stderr.strip()}", file=sys.stderr)
        return False

def main():
    load_env()
    contact = os.getenv("COLLABORATOR_CONTACT") or os.getenv("ALBY_CONTACT")
    sender = os.getenv("SENDER_NAME") or "Nathan"
    
    if not contact:
        print("⚠️ COLLABORATOR_CONTACT is not set in scripts/.env. Please configure it to enable notifications.")
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Usage: python3 notify_alby.py [start|close|custom] [custom_message]")
        sys.exit(1)

    event = sys.argv[1]
    
    if event == "start":
        message = f"💧 {sender} is active on Daily Drip. Pulling latest files from GitHub to start building!"
    elif event == "close":
        message = f"{sender}'s now closing and is out of GitHub."
    elif event == "push":
        message = f"💧 {sender} just pushed to GitHub!"
    elif event == "custom" and len(sys.argv) > 2:
        message = sys.argv[2]
    else:
        print(f"Unknown event type: {event}")
        sys.exit(1)

    send_imessage(contact, message)

if __name__ == "__main__":
    main()

