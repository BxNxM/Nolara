import os
import json
import re
import shutil

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(SCRIPT_DIR, "../configuration/default_config.json")
USER_CONFIG_FILE = os.path.join(SCRIPT_DIR, "../configuration/usr_config.json")


def _validate_user_configration():
    if not os.path.exists(USER_CONFIG_FILE):
        shutil.copy(DEFAULT_CONFIG_FILE, USER_CONFIG_FILE)
        print(f"Copied {DEFAULT_CONFIG_FILE} to {USER_CONFIG_FILE}")
    else:
        print(f"{USER_CONFIG_FILE} already exists\nCheck config updates...")
        _update_config()


def _update_config():
    default_config:dict = {}
    user_config:dict = {}

    # Load configurations from files. Ignore comments in JSON files.
    with open(USER_CONFIG_FILE, 'r') as file:
        user_config = _load_json_without_comments(file.read())
    with open(DEFAULT_CONFIG_FILE, 'r') as file:
        default_config = _load_json_without_comments(file.read())

    # Check if there are new keys in default config that are not in user config.
    new_config_keys = [key for key in default_config if key not in user_config]
    if len(new_config_keys) > 0:
        print("\tUpdate configuration.")
        default_config.update(user_config)  # Update user config with default values
        with open(USER_CONFIG_FILE, 'w') as file:
            json.dump(default_config, file, indent=4)
    else:
        print("\tNo updates needed.")


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
    with open(USER_CONFIG_FILE, 'r') as file:
        config_data = _load_json_without_comments(file.read())
    return config_data


def get(key):
    return load_config().get(key, None)


_validate_user_configration()

if __name__ == "__main__":
    config = load_config()
    print(config)