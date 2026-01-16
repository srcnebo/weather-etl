# API calls with error handling
"""
Extract: Fetch weather data from Open-Meteo API
"""

import requests
from typing import Any
from schemas.weather import CityInput, WeatherAPIResponse


def fetch_weather_data(
    city: CityInput, start_date: str, end_date: str
) -> dict[str, Any]:
    """
    Fetch historical weather data for a city.

    Args:
        city: Validated city with coordinates
        start_date: Format "YYYY-MM-DD"
        end_date: Format "YYYY-MM-DD"

    Returns:
        Raw API response as dictionary
    """
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": city.latitude,
        "longitude": city.longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "precipitation_sum",
            "wind_speed_10m_max",
            "relative_humidity_2m_mean",
        ],
        "timezone": "auto",
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()  # Raises exception for 4xx/5xx

    return response.json()


def validate_api_response(raw_data: dict[str, Any]) -> WeatherAPIResponse:
    """
    Validate API response using Pydantic.
    This catches malformed data before it hits your database.
    """
    daily_data = raw_data.get("daily", {})
    return WeatherAPIResponse(**daily_data)
