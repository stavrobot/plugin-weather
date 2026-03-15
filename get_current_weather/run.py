#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "requests"
# ]
# ///

import json
import sys
import requests


def fetch_weather(latitude: float, longitude: float) -> dict:
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum",
        "forecast_days": 1,
        "timezone": "auto",
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        json.dump({"error": f"Failed to fetch weather data: {str(e)}"}, sys.stdout, indent=2)
        sys.exit(1)


def build_result(latitude: float, longitude: float, data: dict) -> dict:
    current = data["current"]
    daily = data["daily"]

    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": data["timezone"],
        },
        "current": {
            "time": current["time"],
            "temperature_2m": current["temperature_2m"],
            "apparent_temperature": current["apparent_temperature"],
            "relative_humidity_2m": current["relative_humidity_2m"],
            "wind_speed_10m": current["wind_speed_10m"],
            "weather_code": current["weather_code"],
        },
        "today": {
            "temperature_2m_max": daily["temperature_2m_max"][0],
            "temperature_2m_min": daily["temperature_2m_min"][0],
            "sunrise": daily["sunrise"][0],
            "sunset": daily["sunset"][0],
            "precipitation_sum": daily["precipitation_sum"][0],
        },
    }


def main() -> None:
    input_data = json.load(sys.stdin)

    latitude = input_data.get("latitude")
    longitude = input_data.get("longitude")

    if latitude is None:
        json.dump({"error": "latitude is required"}, sys.stdout, indent=2)
        sys.exit(1)

    if longitude is None:
        json.dump({"error": "longitude is required"}, sys.stdout, indent=2)
        sys.exit(1)

    data = fetch_weather(latitude, longitude)
    result = build_result(latitude, longitude, data)
    json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
