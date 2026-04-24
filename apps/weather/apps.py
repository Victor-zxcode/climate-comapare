"""Weather app - Climate data and forecast management"""
from django.apps import AppConfig


class WeatherConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.weather"
    verbose_name = "Weather & Climate"

    def ready(self):
        import apps.weather.signals
