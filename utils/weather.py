

import requests
from config import OPENWEATHER_API_KEY


def fetch_weather(city: str, api_key: str | None = None) -> dict | None:
    """
    Fetch current weather for a city.

    Args:
        city:    City name (e.g. "Mumbai")
        api_key: Optional override — uses config key if not provided

    Returns:
        dict with keys: city, temp, desc, icon
        None if request fails or key is missing
    """
    key = api_key or OPENWEATHER_API_KEY

    if not key or key == "your-openweathermap-key-here":
        return None

    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={key}&units=metric"
        )
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            return {
                "city": data["name"],
                "temp": round(data["main"]["temp"]),
                "desc": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["main"],   # "Clear", "Rain", etc.
            }

        if response.status_code == 401:
            return {"error": "Invalid API key. Check your OpenWeatherMap key."}

        if response.status_code == 404:
            return {"error": f"City '{city}' not found."}

    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Try again."}
    except Exception as e:
        return {"error": str(e)}

    return None
