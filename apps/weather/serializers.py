"""Weather app serializers"""
from rest_framework import serializers
from .models import WeatherForecast, HourlyWeatherData, WeatherComparison
from apps.cities.models import City


class HourlyWeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourlyWeatherData
        fields = ("hour", "temperature", "precipitation", "wind_speed", "humidity")


class WeatherForecastSerializer(serializers.ModelSerializer):
    hourly_data = HourlyWeatherDataSerializer(many=True, read_only=True)
    city_name = serializers.CharField(source="city.name", read_only=True)
    condition_display = serializers.CharField(source="get_weather_code_display", read_only=True)

    class Meta:
        model = WeatherForecast
        fields = (
            "id",
            "city",
            "city_name",
            "date",
            "temp_current",
            "temp_max",
            "temp_min",
            "temp_average",
            "precipitation_sum",
            "precipitation_probability",
            "wind_speed_max",
            "wind_direction",
            "wind_direction_cardinal",
            "humidity",
            "weather_code",
            "condition_display",
            "condition_description",
            "is_current",
            "hourly_data",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "condition_description",
            "wind_direction_cardinal",
            "created_at",
            "updated_at",
        )


class WeatherComparisonSerializer(serializers.ModelSerializer):
    cities_data = serializers.SerializerMethodField()

    class Meta:
        model = WeatherComparison
        fields = ("id", "name", "description", "cities", "cities_data", "created_at", "updated_at")

    def get_cities_data(self, obj):
        """Get latest forecast for each city"""
        cities_forecast = []
        for city in obj.cities.all():
            latest_forecast = (
                WeatherForecast.objects.filter(city=city, is_current=True)
                .first()
            )
            if latest_forecast:
                cities_forecast.append(WeatherForecastSerializer(latest_forecast).data)
        return cities_forecast
