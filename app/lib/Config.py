import os
import json
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


def load_config():
    _user_configration()
    with open(USER_CONFIG_FILE, 'r') as file:
        config_data = json.load(file)
    return config_data


def get(key):
    return load_config().get(key, None)


if __name__ == "__main__":
    config = load_config()
    print(config)