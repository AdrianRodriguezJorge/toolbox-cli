import os
import json

CONFIG_FILE = os.path.expanduser("~/.toolbox_cli.json")

def load_config():
    """Load config from a user-home JSON file, default to English."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"language": "en"}

def save_config(config):
    """Save config dict to JSON."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception:
        pass
