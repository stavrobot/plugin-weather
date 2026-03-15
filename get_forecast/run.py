#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "requests"
# ]
# ///

import json
import sys
import requests

# Open-Meteo supports at most 7 days (offsets 0–6) in the free forecast endpoint.
MAX_DAY_OFFSET = 6


def fetch_forecast(latitude: float, longitude: float, forecast_days: int) -> dict:
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,weather_code",
        "forecast_days": forecast_days,
        "timezone": "auto",
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        json.dump({"error": f"Failed to fetch forecast data: {str(e)}"}, sys.stdout, indent=2)
        sys.exit(1)


def build_result(latitude: float, longitude: float, data: dict, from_day: int, to_day: int) -> dict:
    daily = data["daily"]

    # Zip the parallel daily arrays into per-day dicts, then slice to the requested range.
    days = [
        {
            "date": daily["time"][index],
            "temperature_2m_max": daily["temperature_2m_max"][index],
            "temperature_2m_min": daily["temperature_2m_min"][index],
            "sunrise": daily["sunrise"][index],
            "sunset": daily["sunset"][index],
            "precipitation_sum": daily["precipitation_sum"][index],
            "weather_code": daily["weather_code"][index],
        }
        for index in range(from_day, to_day + 1)
    ]

    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": data["timezone"],
        },
        "forecast": days,
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

    from_day: int = min(max(int(input_data.get("from_day", 1)), 0), MAX_DAY_OFFSET)
    to_day: int = min(max(int(input_data.get("to_day", 6)), 0), MAX_DAY_OFFSET)

    # Open-Meteo returns `forecast_days` days starting from today (offset 0), so we
    # request to_day + 1 days to ensure the last requested day is included in the response.
    data = fetch_forecast(latitude, longitude, to_day + 1)
    result = build_result(latitude, longitude, data, from_day, to_day)
    json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
