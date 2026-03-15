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

    # Get city name (required)
    city = input_data.get("city")

    if not city:
        error_result = {
            "error": "City name is required"
        }
        json.dump(error_result, sys.stdout, indent=2)
        sys.exit(1)

    # Build API URL
    base_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city,
        "count": 5,
        "language": "en",
        "format": "json"
    }

    try:
        # Make API request
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extract results
        results = data.get("results", [])

        if not results:
            result = {
                "message": f"No locations found for '{city}'",
                "locations": []
            }
            json.dump(result, sys.stdout, indent=2)
            return

        # Format locations
        locations = []
        for loc in results:
            location = {
                "name": loc.get("name", ""),
                "country": loc.get("country", ""),
                "latitude": loc.get("latitude"),
                "longitude": loc.get("longitude"),
                "population": loc.get("population"),
                "timezone": loc.get("timezone", "")
            }

            # Add state/region if available (useful for disambiguation).
            if "admin1" in loc:
                location["admin1"] = loc["admin1"]

            locations.append(location)

        # Build result
        result = {
            "query": city,
            "count": len(locations),
            "locations": locations
        }

        # Output result
        json.dump(result, sys.stdout, indent=2)

    except requests.exceptions.RequestException as e:
        error_result = {
            "error": f"Failed to fetch geocoding data: {str(e)}"
        }
        json.dump(error_result, sys.stdout, indent=2)
        sys.exit(1)

if __name__ == "__main__":
    main()
