"""Weather app models"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.cities.models import City
import logging

logger = logging.getLogger(__name__)


class WeatherForecast(models.Model):
    """Store weather forecast data"""

    CONDITION_CHOICES = (
        (0, "Céu limpo"),
        (1, "Parcialmente nublado"),
        (2, "Nublado"),
        (3, "Encoberto"),
        (45, "Nevoeiro"),
        (48, "Nevoeiro com deposição de gelo"),
        (51, "Chuvisco leve"),
        (53, "Chuvisco moderado"),
        (55, "Chuvisco denso"),
        (61, "Chuva leve"),
        (63, "Chuva moderada"),
        (65, "Chuva forte"),
        (71, "Neve leve"),
        (73, "Neve moderada"),
        (75, "Neve forte"),
    )

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="forecasts")
    date = models.DateField(db_index=True)

    # Temperature
    temp_current = models.FloatField(
        validators=[MinValueValidator(-60), MaxValueValidator(60)]
    )
    temp_max = models.FloatField(
        validators=[MinValueValidator(-60), MaxValueValidator(60)]
    )
    temp_min = models.FloatField(
        validators=[MinValueValidator(-60), MaxValueValidator(60)]
    )
    temp_average = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(-60), MaxValueValidator(60)]
    )

    # Precipitation
    precipitation_sum = models.FloatField(
        validators=[MinValueValidator(0)], default=0
    )  # mm
    precipitation_probability = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], default=0
    )  # %

    # Wind
    wind_speed_max = models.FloatField(validators=[MinValueValidator(0)])  # km/h
    wind_direction = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(360)], default=0
    )  # degrees
    wind_direction_cardinal = models.CharField(max_length=3, default="N")  # N, NE, E, etc

    # Humidity
    humidity = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], default=0
    )  # %

    # Weather condition
    weather_code = models.IntegerField(
        choices=CONDITION_CHOICES, default=0, db_index=True
    )
    condition_description = models.CharField(max_length=100, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_current = models.BooleanField(default=False, db_index=True)

    class Meta:
        verbose_name = "Weather Forecast"
        verbose_name_plural = "Weather Forecasts"
        unique_together = ("city", "date")
        ordering = ("-date",)
        indexes = [
            models.Index(fields=["city", "-date"]),
            models.Index(fields=["date"]),
        ]

    def __str__(self):
        return f"{self.city.name} - {self.date} ({self.get_weather_code_display()})"

    @staticmethod
    def get_cardinal_direction(degrees):
        """Convert degrees to cardinal direction"""
        directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                      "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        idx = round(degrees / 22.5) % 16
        return directions[idx]


class HourlyWeatherData(models.Model):
    """Store hourly weather data"""

    forecast = models.ForeignKey(
        WeatherForecast, on_delete=models.CASCADE, related_name="hourly_data"
    )
    hour = models.TimeField()

    temperature = models.FloatField(
        validators=[MinValueValidator(-60), MaxValueValidator(60)]
    )
    precipitation = models.FloatField(validators=[MinValueValidator(0)])  # mm
    wind_speed = models.FloatField(validators=[MinValueValidator(0)])  # km/h
    humidity = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )  # %

    class Meta:
        verbose_name = "Hourly Weather Data"
        verbose_name_plural = "Hourly Weather Data"
        unique_together = ("forecast", "hour")
        ordering = ["hour"]

    def __str__(self):
        return f"{self.forecast.city.name} - {self.hour}"


class WeatherComparison(models.Model):
    """Store user-created weather comparisons"""

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, blank=True)
    cities = models.ManyToManyField(City, related_name="comparisons")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Weather Comparison"
        verbose_name_plural = "Weather Comparisons"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
