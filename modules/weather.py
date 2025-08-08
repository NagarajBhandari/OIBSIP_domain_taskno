# weather.py
import requests

def get_weather_summary(location, api_key):
    # location: city name string; if "your location" => return generic message
    if not api_key or "YOUR_OPENWEATHERMAP_API_KEY" in api_key:
        return "Weather API key not configured. Please add your OpenWeatherMap API key in config.py."

    if not location or location.lower() in ("your location", "here"):
        return "Please tell me the city name for weather information (e.g., 'weather in London')."

    # OpenWeatherMap current weather endpoint
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": api_key, "units": "metric"}
    try:
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        j = r.json()
        desc = j["weather"][0]["description"]
        temp = j["main"]["temp"]
        feels = j["main"]["feels_like"]
        return f"Current weather in {location.title()}: {desc}, {temp}°C, feels like {feels}°C."
    except requests.HTTPError as e:
        return f"Couldn't fetch weather for {location}. ({e})"
    except Exception as e:
        return f"Weather service error: {e}"
