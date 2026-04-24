"""Weather app views"""
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import WeatherForecast, WeatherComparison
from .serializers import WeatherForecastSerializer, WeatherComparisonSerializer
import logging

logger = logging.getLogger(__name__)


class WeatherForecastViewSet(viewsets.ModelViewSet):
    """ViewSet for WeatherForecast"""

    queryset = WeatherForecast.objects.select_related("city").prefetch_related(
        "hourly_data"
    )
    serializer_class = WeatherForecastSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["city", "date", "is_current"]
    ordering = ["-date"]
    ordering_fields = ["date", "temp_current", "wind_speed_max"]


class WeatherComparisonViewSet(viewsets.ModelViewSet):
    """ViewSet for WeatherComparison"""

    queryset = WeatherComparison.objects.prefetch_related("cities")
    serializer_class = WeatherComparisonSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering = ["-created_at"]
