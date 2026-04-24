"""Weather app signals"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WeatherForecast, HourlyWeatherData
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=WeatherForecast)
def update_condition_description(sender, instance, created, **kwargs):
    """Update condition description when weather forecast is created/updated"""
    instance.condition_description = instance.get_weather_code_display()
    instance.wind_direction_cardinal = WeatherForecast.get_cardinal_direction(
        instance.wind_direction
    )
    if created or not kwargs.get("raw", False):
        instance.save(update_fields=["condition_description", "wind_direction_cardinal"])
