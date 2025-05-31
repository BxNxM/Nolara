
'''
def set_color(r: int, g: int, b: int) -> dict:
    """
    SET RGB color

    Args:
      r: red color channel 0-255
      g: green color channel 0-255
      b: blue color channel 0-255

    Returns:
      dict: RGB color dictionary {"r": r, "g": g, "b": b}
    """
    color = {"r": r, "g": g, "b": b}
    print(f"Color: {color}")
    return color
'''


def set_rgb_color(device: str, r: int, g: int, b: int) -> str:
    """
    Set an RGB color on a remote device.

    Args:
        device (str): Name or ID of the target device
        r (int): Red value (0-255)
        g (int): Green value (0-255)
        b (int): Blue value (0-255)

    Returns:
        str: Confirmation message
    """
    # Simulate setting color (replace with real device logic / API call)
    if device not in DEVICE_REGISTRY:
        print(f"DEVICE NOT FOUND: {device}")
        #raise ValueError(f"Device '{device}' not found.")

    # Here you'd send the color command to the real device
    print(f"Setting color for {device}: R={r}, G={g}, B={b}")

    return f"Color set to ({r}, {g}, {b}) on device '{device}'."


def list_devices() -> list[dict]:
    """
    List available RGB-capable devices with metadata.

    Returns:
        list[dict]: Each device includes name, location, and features
    """
    return [
        {
            "name": "lamp_livingroom",
            "location": "Living Room",
            "features": ["color", "brightness"]
        },
        {
            "name": "ceiling_kitchen",
            "location": "Kitchen",
            "features": ["color"]
        },
        {
            "name": "strip_bedroom",
            "location": "Bedroom",
            "features": ["color", "animation"]
        }
    ]


DEVICE_REGISTRY = {device["name"]: device for device in list_devices()}

