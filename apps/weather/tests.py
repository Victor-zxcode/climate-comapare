"""Weather app tests"""
from django.test import TestCase
from django.utils import timezone
from apps.cities.models import City
from .models import WeatherForecast


class WeatherForecastTestCase(TestCase):
    def setUp(self):
        self.city = City.objects.create(
            name="Test City",
            country="Test Country",
            latitude=0.0,
            longitude=0.0,
        )

    def test_create_forecast(self):
        forecast = WeatherForecast.objects.create(
            city=self.city,
            date=timezone.now().date(),
            temp_current=25.0,
            temp_max=28.0,
            temp_min=20.0,
            wind_speed_max=15.0,
            humidity=60,
            weather_code=0,
        )
        self.assertEqual(forecast.city.name, "Test City")
        self.assertEqual(forecast.temp_current, 25.0)

    def test_cardinal_direction(self):
        direction = WeatherForecast.get_cardinal_direction(45)
        self.assertEqual(direction, "NE")
