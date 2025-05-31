# Allow math functions
import math
import requests
from datetime import datetime


def calculator(expression: str) -> float:
    """
    Safely evaluate a basic Python mathematical expression.

    Args:
        expression (str): A mathematical expression, e.g. "2 + 3 * (4 - 1)"

    Returns:
        float: The result of the evaluated expression

    Raises:
        ValueError: If the expression contains disallowed operations or is invalid
    """
    allowed_names = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "__builtins__": {},  # Disable all built-in functions unless explicitly allowed
    }
    allowed_names.update({k: getattr(math, k) for k in dir(math) if not k.startswith("_")})

    try:
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return result
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")


def get_weather(location: str) -> dict:
    """
    Get current weather using wttr.in (no API key required).

    Args:
        location (str): Location name, e.g., "Budapest"

    Returns:
        dict: Basic weather info including temperature and condition
    """
    url = f"https://wttr.in/{location}?format=j1"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch weather for {location}")

    data = response.json()
    current = data["current_condition"][0]

    return {
        "location": location,
        "temperature_celsius": float(current["temp_C"]),
        "condition": current["weatherDesc"][0]["value"],
        "humidity_percent": int(current["humidity"])
    }


def get_current_datetime() -> dict:
    """
    Return the current date and time.

    Returns:
        dict: Contains ISO datetime string and separate components.
    """
    now = datetime.now()
    return {
        "iso": now.isoformat(),  # e.g. "2025-05-31T14:25:36.123456"
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": now.hour,
        "minute": now.minute,
        "second": now.second
    }


def get_location_from_user() -> str:
    """
    Get approximate user location by IP using ipinfo.io.

    Returns:
        str: Location name (city) or fallback default.
    """
    try:
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            city = data.get("city")
            if city:
                return city
    except Exception as e:
        return f"Location detection failed: {e}"

