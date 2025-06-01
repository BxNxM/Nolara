import os
import json
import re
import shutil

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(SCRIPT_DIR, "../configuration/default_config.json")
USER_CONFIG_FILE = os.path.join(SCRIPT_DIR, "../configuration/usr_config.json")


def _user_configration():
    if not os.path.exists(USER_CONFIG_FILE):
        shutil.copy(DEFAULT_CONFIG_FILE, USER_CONFIG_FILE)
        print(f"Copied {DEFAULT_CONFIG_FILE} to {USER_CONFIG_FILE}")
    else:
        print(f"{USER_CONFIG_FILE} already exists")


def _load_json_without_comments(jsonc: str) -> dict:
    """
    Support json file with line comments //
    Args:
        jsonc: json file content as string
    Returns:
        dict object
    """
    # Remove // comments (both full-line and inline)
    cleaned = re.sub(r'//.*', '', jsonc)
    # Optionally strip extra whitespace
    cleaned = cleaned.strip()
    # Parse to valid JSON
    parsed = json.loads(cleaned)
    return parsed


def load_config():
    _user_configration()
    with open(USER_CONFIG_FILE, 'r') as file:
        config_data = _load_json_without_comments(file.read())
    return config_data


def get(key):
    return load_config().get(key, None)


if __name__ == "__main__":
    config = load_config()
    print(config)