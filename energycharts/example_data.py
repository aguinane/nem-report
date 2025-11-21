
import calendar
from datetime import date, datetime, timedelta
from random import randint

import polars as pl


def get_days_in_year(year: int) -> list[date]:
  """Get all days in a given yearas a list of date objects."""
  xday= date(year, 1, 1)
  num_days= 366 if calendar.isleap(year) else 365
  days = []
  for i in range(num_days):
    current_day= xday+ timedelta(days=i)
    days.append(current_day)
  return days

def generate_example_daily_usage_data(
  year: int = 2025, include_export: bool = False
) -> pl.DataFrame:
  """Returns example values for each day in a year"""
  example_data= []
  for day in get_days_in_year(year):
    imp_kwh= randint(1000, 13000) / 1000
    exp_kwh= -1 * randint(0, 10000) / 1000  if include_export else 0
    total_kwh= imp_kwh+ exp_kwh
    row = (day, total_kwh)
    example_data.append(row)

  return pl.DataFrame(example_data, schema=["date", "value"])

def get_day_intervals(day: date, interval: int = 5) -> list[datetime]:
  """Get all days in a given yearas a list of date objects."""

  intervals = []
  xday= datetime(day.year, day.month, day.day)
  end = xday+ timedelta(days=1)

  while xday< end:
    intervals.append(xday)
    xday+= timedelta(minutes=interval)
  return intervals

def estimate_export(month: int, hour: int, interval: int) -> float:
  """Estimate export kWh for a given hour of the day"""
  conv = interval / 60
  max_value = 5000 if 3 <= month <= 5 or 9 <= month <= 11 else 4000
  if 10 <= hour < 14 or 6 <= hour < 18:
    return randint(0, max_value) / 1000 * conv
  return 0.0

def estimate_import(month: int, hour: int, interval: int) -> float:
  """Estimate export kWh for a given hour of the day"""
  conv = interval / 60
  max_morning_value = 7000 if 6 <= month <= 9 else 4000
  max_evening_value = 8000 if month in (1,2,11,12) else 5000
  if 16 <= hour < 20:
    return randint(0, max_evening_value) / 1000 * conv
  elif 6 <= hour < 9:
    return randint(0, max_morning_value) / 1000 * conv
  elif 20 <= hour < 22 or 11 <= hour < 14:
    return randint(0, 3000) / 1000 * conv
  return randint(0, 2000) / 1000 * conv

def generate_example_profile_data(
  year: int = 2025, include_export: bool = True
) -> pl.DataFrame:
  """Returns example values for a year"""
  example_data= []
  interval = 5
  for day in get_days_in_year(year):
    for period in get_day_intervals(day, interval):
      
      xhour= period.hour
      xmonth = period.month
      imp_kwh= estimate_import(xmonth, xhour, interval)
      exp_kwh=  -1 * estimate_export(xmonth, xhour, interval) if include_export else 0
      total_kwh= imp_kwh+ exp_kwh
      row = (period, total_kwh)
      example_data.append(row)

  return pl.DataFrame(example_data, schema=["ts", "value"], orient="row")


