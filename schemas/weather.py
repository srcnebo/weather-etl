"""
Pydantic models for weather data validation.
Think of these like TypeScript interfaces — they enforce structure.
"""
from datetime import date
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class WeatherAPIResponse(BaseModel):
  """Validates raw data coming from Open-Meteo API"""
  time: list[str]
  temperature_2m_max: list[float]
  temperature_2m_min: list[float]
  temperature_2m_mean: list[float]
  precipitation_sum: list[float]
  wind_speed_10m_max: list[float]
  relative_humidity_2m_mean: list[float]


class CityInput(BaseModel):
  """Validates city configuration"""
  name: str = Field(..., min_length=1)
  latitude: float = Field(..., ge=-90, le=90)
  longitude: float = Field(..., ge=-180, le=180)
  country: str = Field(default="Unknown")

  @field_validator('name')
  @classmethod
  def name_must_be_title_case(cls, v: str) -> str:
    return v.strip().title()


class WeatherRecord(BaseModel):
  """A single day's weather for one city — ready for database"""
  city_name: str
  date: date
  temp_max: float
  temp_min: float
  temp_mean: float
  precipitation: float
  wind_speed: float
  humidity: float

  @field_validator('temp_max')
  @classmethod
  def temp_max_reasonable(cls, v: float) -> float:
    if v < -100 or v > 60:
      raise ValueError(f"Temperature {v}°C seems unreasonable")
    return v