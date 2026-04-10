import json
import urllib.request

# --- Math Tools ---

def add(a, b):
    """Add two numbers."""
    return {"operation": "addition", "a": a, "b": b, "result": a + b}

def subtract(a, b):
    """Subtract b from a."""
    return {"operation": "subtraction", "a": a, "b": b, "result": a - b}

def multiply(a, b):
    """Multiply two numbers."""
    return {"operation": "multiplication", "a": a, "b": b, "result": a * b}

def divide(a, b):
    """Divide a by b with zero-check."""
    if b == 0:
        return {"operation": "division", "a": a, "b": b, "error": "Cannot divide by zero"}
    return {"operation": "division", "a": a, "b": b, "result": a / b}

# --- Weather Tool ---

def get_weather(city):
    """Fetch weather from wttr.in for a given city."""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        current = data["current_condition"][0]
        return {
            "city": city,
            "temp_c": current["temp_C"],
            "feels_like_c": current["FeelsLikeC"],
            "description": current["weatherDesc"][0]["value"],
            "humidity": current["humidity"],
            "wind_kmph": current["windspeedKmph"],
        }
    except Exception as e:
        return {"city": city, "error": f"Could not fetch weather: {e}"}
