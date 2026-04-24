"""Cities app models"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import logging

logger = logging.getLogger(__name__)


class City(models.Model):
    """City model for storing geographic locations"""

    name = models.CharField(max_length=100, db_index=True)
    country = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=100, blank=True)

    # Geographic coordinates
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )

    # Timezone
    timezone = models.CharField(max_length=50, default="UTC")

    # Metadata
    population = models.IntegerField(null=True, blank=True)
    is_capital = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_weather_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        unique_together = ("name", "country", "latitude", "longitude")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name", "country"]),
            models.Index(fields=["is_capital"]),
        ]

    def __str__(self):
        return f"{self.name}, {self.country}"

    @property
    def full_location(self):
        """Return full location string"""
        return f"{self.name}, {self.state or ''} {self.country}".replace("  ", " ").strip()


class CityAlias(models.Model):
    """Alternative names for cities"""

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="aliases")
    alias = models.CharField(max_length=100, unique=True, db_index=True)

    class Meta:
        verbose_name = "City Alias"
        verbose_name_plural = "City Aliases"

    def __str__(self):
        return f"{self.alias} → {self.city.name}"
