from _micrOS_common import load_device_config, run_command_on_device

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
    Generic function to execute a remote command on a device.
    Always check the command against list_remote_devices[x][metadata][feature_calls] before calling this function.

    Args:
        device: device name
        command: command to be executed on the remote device, from list_remote_devices[x][metadata][feature_calls]

    Returns:
      dict: response from the device after command execution
    """
    response = run_command_on_device(device, command)
    response['command'] = command  # Add the executed command to the response for logging or debugging purposes.
    return response


def list_remote_devices() -> list[dict]:
    """
    List available remote devices for run_command_on_device tool call.
    Returned device name to be used as device parameter of run_command_on_device function call.
    Each device is a dictionary with the following keys:
        name (str): Name of the device
        metadata (dict): Dictionary containing additional information about the device, including location and features.

    Returns:
        list[dict]: Each device includes name, location, and features
    """

    return load_device_config()
