from micros_interface._micrOS_common import (load_device_config,
                                             run_command_on_device,
                                             auto_feature_discovery)

'''
def color_setter(device: str, r: int, g: int, b: int) -> dict:
    """
    If user asks for light color change.
    Features: color

    Args:
      device: device name
      r: red color channel 0-255
      g: green color channel 0-255
      b: blue color channel 0-255

    Returns:
      dict: response from the device after setting color
    """
    color_command = f"rgb color {r} {g} {b}"
    response = run_command_on_device(device, color_command)
    return response


def brightness_setter(device: str, brightness: int) -> dict:
    """
    If user asks for light brightness change.
    Features: brightness

    Args:
      device: device name
      brightness: brightness level 0-100

    Returns:
      dict: response from the device after setting brightness
    """
    brightness_command = f"rgb brightness {brightness}"
    response = run_command_on_device(device, brightness_command)
    return response
'''

def generic_remote_command_executor(device: str, command: str) -> dict:
    """
    USE THIS TOOL FOR MICROS COMMAND EXECUTION
    Always check the command against list_micros_device_features(device)
        [metadata][feature_calls] show command templates

    Args:
        device: Name of the micros device (micros_device_name or device_name)
        command: command to be executed on the remote device, from list_micros_device_features[metadata][feature_calls]

    Returns:
      dict: response from the device after command execution
    """
    response = run_command_on_device(device, command)
    response['command'] = command  # Add the executed command to the response for logging or debugging purposes.
    return response


def list_micros_devices() -> list[dict]:
    """
    List available remote devices for list_micros_device_features and generic_remote_command_executor.
    Each device is a dictionary with micrOS device_name and metadata[location] additional info.

    Returns:
        list[dict]: device list [{device_name: "device1", metadata: {"location": "room1"}}, ...]
    """

    device_list = []
    device_config = load_device_config()
    for device in device_config:
        device_name = device["device_name"]
        device_location = device["metadata"]["location"]
        device_list.append({"device_name": device_name, "metadata": {"location": device_location}})
    return device_list


def list_micros_device_features(device: str) -> dict:
    """
    List available features of a specific micros device.
    This function can be called when generic_remote_command_executor tool command is needed.
    Output can be used to construct a command executor tool command input.

    Args:
        device: Name of the micros device (device_name)

    Returns:
        dict: Dictionary with available features of the micros device.
    """
    device_config = load_device_config()
    for device_cfg in device_config:
        device_name = device_cfg["device_name"]
        if device_name == device:
            return device_cfg
    return {}


def run_device_feature_discovery():
    """
    Automatically discover features of all connected devices.
    This function can be called when user asks for refreshing device feature list.
    User approval is needed to call this function!

    Returns:
        list[dict]: Each device includes name, location, and features
    """

    return auto_feature_discovery()
