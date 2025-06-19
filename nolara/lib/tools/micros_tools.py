from _micrOSClient import micrOSClient


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
    response = _run_command_on_device(device, color_command)
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
    response = _run_command_on_device(device, brightness_command)
    return response


def _run_command_on_device(device: str, command: str) -> dict:
    """
    Args:
        device (str): Name of the device
        command (str): Command to run, structure: <module> <function> <*params>
    Returns:
        dict: Response from the device, structure: {"status": "success"|"error", "response": <response>}
    """
    """
    com_obj = micrOSClient(host=device, port=9008, pwd="ADmin123", dbg=True)
    try:
        response = com_obj.send_cmd(command)
    except Exception as e:
        response = {"status": "error", "response": str(e)}
    """
    com_obj = micrOSClient(host=device, port=9008, pwd="ADmin123", dbg=False)
    response = com_obj.send_cmd(command, timeout=3, retry=5, stream=False)
    return {"status": "success", "response": response, "device": device}


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
    return [
        {
            "device_name": "LivingKitchen.local",
            "metadata": {
                "location": "Living Room",
                "features": ["color", "brightness"]
            }
        },
        {
            "device_name": "Cabinet.local",
            "metadata": {
                "location": "Kitchen",
                "features": ["color"]
            }
        }
    ]
