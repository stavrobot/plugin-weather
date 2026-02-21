# Weather plugin

A Stavrobot plugin that provides weather data using the Open-Meteo API. No API key required.

## Installation

Ask Stavrobot to install git@github.com:stavrobot/plugin-weather.git.

## Tools

### geocode

Converts a city name to geographic coordinates.

**Parameters:**
- `city` (string, required): The city name to search for.

**Returns:** Up to 5 matching locations with coordinates, country, timezone, and administrative regions.

### get_weather

Fetches current weather conditions and today's forecast for a location.

**Parameters:**
- `latitude` (number): Latitude coordinate. Defaults to Thessaloniki, Greece (40.6401).
- `longitude` (number): Longitude coordinate. Defaults to Thessaloniki, Greece (22.9444).

**Returns:** Current temperature, apparent temperature, humidity, wind speed, weather code, and today's high/low temperatures, sunrise/sunset times, and precipitation.

## Usage

Use `geocode` first to find coordinates for a city, then pass those coordinates to `get_weather`.
