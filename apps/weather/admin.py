"""Weather app - Admin configuration"""
from django.contrib import admin
from .models import WeatherForecast, HourlyWeatherData, WeatherComparison


@admin.register(WeatherForecast)
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = (
        "city",
        "date",
        "temp_current",
        "condition_description",
        "wind_speed_max",
        "is_current",
    )
    list_filter = ("date", "is_current", "weather_code", "city")
    search_fields = ("city__name",)
    readonly_fields = ("created_at", "updated_at", "condition_description")

    fieldsets = (
        ("Basic Information", {"fields": ("city", "date", "is_current")}),
        (
            "Temperature",
            {
                "fields": (
                    "temp_current",
                    "temp_max",
                    "temp_min",
                    "temp_average",
                )
            },
        ),
        (
            "Precipitation",
            {
                "fields": (
                    "precipitation_sum",
                    "precipitation_probability",
                )
            },
        ),
        (
            "Wind",
            {
                "fields": (
                    "wind_speed_max",
                    "wind_direction",
                    "wind_direction_cardinal",
                )
            },
        ),
        ("Humidity & Condition", {"fields": ("humidity", "weather_code", "condition_description")}),
        ("Metadata", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(HourlyWeatherData)
class HourlyWeatherDataAdmin(admin.ModelAdmin):
    list_display = ("forecast", "hour", "temperature", "precipitation", "wind_speed")
    list_filter = ("forecast__date", "hour")
    search_fields = ("forecast__city__name",)


@admin.register(WeatherComparison)
class WeatherComparisonAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    filter_horizontal = ("cities",)
    search_fields = ("name",)
