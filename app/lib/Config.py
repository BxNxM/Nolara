import os
import json

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(SCRIPT_DIR, "../config.json")

def load_config():
    with open(CONFIG_DIR, 'r') as file:
        config_data = json.load(file)
    return config_data


def get(key):
    return load_config().get(key, None)


if __name__ == "__main__":
    config = load_config()
    print(config)