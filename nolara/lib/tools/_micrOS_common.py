import ast
import json
from pathlib import Path

from _micrOSClient import micrOSClient
from pprint import pprint

DEVICE_CLIS = {}
TOOL_CONFIG = Path(__file__).parent / "_micrOS_devices.json"


def _feature_discovery(device: str) -> (list, list):
    """
    GENERIC MICROS FEATURE DISCOVER

    LivingKitchen $ modules
    ['rgbcct', 'dimmer', 'rgb', 'cct', 'dashboard_be', 'system', 'intercon', 'task']

    LivingKitchen $ rgb help widgets=True
        {"lm_call": "color r=:range: g=:range: b=:range: smooth=True force=True", "type": "color", "range": [0, 1000, 10]},
        {"lm_call": "toggle state=:options: smooth=True", "type": "button", "options": ["True", "False"]},
        {"lm_call": "brightness percent=:range: smooth=True wake=True", "type": "slider", "range": [0, 100, 2]},
        {"lm_call": "random smooth=True max_val=1000", "type": "button", "options": ["None"]},
    """

    # Fetch loaded modules from the device
    loaded_modules = []
    features_call_table = []
    feature_list = set()
    response = run_command_on_device(device=device, command="modules")
    if response["status"] == "success":
        loaded_modules = response["response"][0]
        try:
            print(f"Raw modules response data: {loaded_modules} {type(loaded_modules)}")
            loaded_modules = ast.literal_eval(loaded_modules)
            print(f"Parsed modules response data: {loaded_modules} {type(loaded_modules)}")
        except Exception as e:
            print(f"_feature_discovery error: {e}")
    else:
        print(f"_feature_discovery error: {response}")

    # Iterate through each module and its functions to discover features
    for module in loaded_modules:
        functions_cmd = f"{module} help widgets=True"
        response = run_command_on_device(device=device, command=functions_cmd)
        if response["status"] == "success":
            widgets = response["response"]
            for raw_widget in widgets:
                try:
                    # Ignore non json inputs
                    if not raw_widget.strip().startswith('{'):
                        print(f"\tSKIP: Non-JSON input: {device}: {module} {raw_widget}")
                        continue
                    # Strip trailing comma if present
                    if raw_widget.strip().endswith(','):
                        raw_widget = raw_widget.strip().rstrip(',')
                    widget = json.loads(raw_widget)
                    _lm_call = f"{module} {widget["lm_call"]}"
                    _range = widget.get("range")
                    _options = widget.get("options")
                    #print(f"Module: {module}, _lm_call: {_lm_call} _range: {_range} _options: {_options}")
                    feature_data = {"command": _lm_call, "description": "Command can be called without modification."}
                    if _range is not None:
                        feature_data["range"] = _range
                        feature_data["description"] = "range[0]=min value, range[1]=max value, range[2]=step value, Replace :range: with actual range values"
                    if _options is not None:
                        feature_data["options"] = _options
                        feature_data["description"] = "options[0]=option1, options[1]=option2, etc. Replace :options: with actual options values"
                    features_call_table.append(feature_data)
                    feature_list.add(widget["lm_call"].split()[0])
                except Exception as e:
                    print(f"widget parse error: {e}\ndata: {raw_widget}")
        else:
            print(f"_feature_discovery error: {response}")

    return features_call_table, list(feature_list)

def run_command_on_device(device: str, command: str) -> dict:
    """
    Args:
        device (str): Name of the device
        command (str): Command to run, structure: <module> <function> <*params>
    Returns:
        dict: Response from the device, structure: {"status": "success"|"error", "response": <response>}
    """

    com_obj = DEVICE_CLIS.get(device, None)
    if com_obj is None:
        com_obj = micrOSClient(host=device, port=9008, pwd="ADmin123", dbg=False)
        DEVICE_CLIS[device] = com_obj
    try:
        response = com_obj.send_cmd(command, timeout=3, retry=5, stream=False)
    except Exception as e:
        response = str(e)
    return {"status": "success", "response": response, "device": device}


def load_device_config():
    """
    Returns:
    [{
        "device_name": "LivingKitchen.local",
        "metadata": {
            "location": "Living Room",
            "features": ["color", "brightness"],
            "feature_calls": []
        }
    },
    ...
    ]
    """

    default_config = [{
        "device_name": "__simulator__",
        "metadata": {
            "location": "simulation",
            "features": ["color", "brightness"],
            "feature_calls": []
            }
        }]

    try:
        with open(TOOL_CONFIG, "r") as f:
            config_data = json.load(f)
        return config_data
    except Exception as e:
        print(f"Error loading device configuration: {e}")
        try:
            with open(TOOL_CONFIG, "w") as f:
                json.dump(default_config, f, indent=4)
        except Exception as e:
            print(f"Error creating default device configuration file: {e}")
    return default_config


def auto_feature_discovery(update_config=False):
    config = load_device_config()
    for index, device in enumerate(config):
        device_name = device["device_name"]
        features_details, features = _feature_discovery(device_name)
        config[index]["metadata"]["features"] = features
        config[index]["metadata"]["feature_calls"] = features_details
    if update_config:
        with open(TOOL_CONFIG, "w") as f:
            json.dump(config, f, indent=4)
    return config


def _test():
    # Example usage:
    tool_config = auto_feature_discovery(update_config=True)
    for tc in tool_config:
        pprint(tc)


if __name__ == "__main__":
    _test()