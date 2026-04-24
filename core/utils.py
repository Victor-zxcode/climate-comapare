"""Utility functions and helpers"""
import logging
from typing import Optional, Dict, Tuple
from core.constants import CARDINAL_DIRECTIONS

logger = logging.getLogger(__name__)


def get_cardinal_direction(degrees: float) -> str:
    """Convert degrees to cardinal direction"""
    if not isinstance(degrees, (int, float)):
        return "N"
    try:
        idx = round(degrees / 22.5) % 16
        return CARDINAL_DIRECTIONS[idx]
    except (IndexError, TypeError):
        return "N"


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32


def celsius_to_kelvin(celsius: float) -> float:
    """Convert Celsius to Kelvin"""
    return celsius + 273.15


def format_temperature(temp: float, unit: str = "C") -> str:
    """Format temperature with unit"""
    if unit == "F":
        temp = celsius_to_fahrenheit(temp)
        unit_symbol = "°F"
    elif unit == "K":
        temp = celsius_to_kelvin(temp)
        unit_symbol = "K"
    else:
        unit_symbol = "°C"
    return f"{temp:.1f}{unit_symbol}"


def calculate_avg_temperature(temps: list) -> Optional[float]:
    """Calculate average temperature"""
    if not temps:
        return None
    try:
        return sum(temps) / len(temps)
    except (TypeError, ValueError):
        logger.error("Error calculating average temperature")
        return None


def validate_coordinates(latitude: float, longitude: float) -> Tuple[bool, Optional[str]]:
    """Validate geographic coordinates"""
    try:
        lat = float(latitude)
        lon = float(longitude)

        if not -90 <= lat <= 90:
            return False, "Latitude must be between -90 and 90"
        if not -180 <= lon <= 180:
            return False, "Longitude must be between -180 and 180"

        return True, None
    except (TypeError, ValueError):
        return False, "Invalid coordinate format"


def generate_cache_key(prefix: str, *args) -> str:
    """Generate cache key from prefix and arguments"""
    parts = [prefix] + [str(arg) for arg in args]
    return ":".join(parts).lower()
