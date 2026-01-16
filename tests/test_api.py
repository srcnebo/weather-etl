"""Quick test to verify API connectivity"""
import requests

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 40.7128,  # New York
    "longitude": -74.0060,
    "start_date": "2024-01-01",
    "end_date": "2024-01-07",
    "daily": ["temperature_2m_max", "temperature_2m_min"],
    "timezone": "auto"
}

response = requests.get(url, params=params)
print(f"Status: {response.status_code}")
print(f"Data: {response.json()['daily']}")