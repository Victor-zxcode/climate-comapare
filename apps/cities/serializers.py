"""Cities app serializers"""
from rest_framework import serializers
from .models import City, CityAlias


class CityAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityAlias
        fields = ("id", "alias")


class CitySerializer(serializers.ModelSerializer):
    aliases = CityAliasSerializer(many=True, read_only=True)
    full_location = serializers.CharField(read_only=True)

    class Meta:
        model = City
        fields = (
            "id",
            "name",
            "country",
            "state",
            "latitude",
            "longitude",
            "timezone",
            "population",
            "is_capital",
            "full_location",
            "aliases",
            "created_at",
            "updated_at",
            "last_weather_update",
        )
        read_only_fields = ("created_at", "updated_at", "last_weather_update")
