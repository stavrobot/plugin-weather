#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "requests"
# ]
# ///

import json
import sys
import requests

def main():
    # Read input parameters
    input_data = json.load(sys.stdin)

    # Get latitude and longitude with defaults (Thessaloniki, Greece)
    latitude = input_data.get("latitude", 40.6401)
    longitude = input_data.get("longitude", 22.9444)

    # Build API URL
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum",
        "timezone": "auto"
    }

    try:
        # Make API request
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extract current weather
        current = data.get("current", {})

        # Extract today's daily forecast (first element in daily arrays)
        daily = data.get("daily", {})
        today_forecast = {}
        if daily:
            for key, values in daily.items():
                if values and len(values) > 0:
                    today_forecast[key] = values[0]

        # Build clean result
        result = {
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "timezone": data.get("timezone", "")
            },
            "current": {
                "time": current.get("time", ""),
                "temperature_2m": current.get("temperature_2m"),
                "apparent_temperature": current.get("apparent_temperature"),
                "relative_humidity_2m": current.get("relative_humidity_2m"),
                "wind_speed_10m": current.get("wind_speed_10m"),
                "weather_code": current.get("weather_code")
            },
            "today_forecast": today_forecast
        }

        # Output result
        json.dump(result, sys.stdout, indent=2)

    except requests.exceptions.RequestException as e:
        error_result = {
            "error": f"Failed to fetch weather data: {str(e)}"
        }
        json.dump(error_result, sys.stdout, indent=2)
        sys.exit(1)
    except Exception as e:
        error_result = {
            "error": f"Unexpected error: {str(e)}"
        }
        json.dump(error_result, sys.stdout, indent=2)
        sys.exit(1)

if __name__ == "__main__":
    main()
