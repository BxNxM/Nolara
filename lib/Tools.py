# Define the Agent Function
def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers

    Args:
      a: The first integer number
      b: The second integer number

    Returns:
      int: The sum of the two numbers
    """
    return a + b

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