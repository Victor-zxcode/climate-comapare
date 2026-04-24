"""API v1 URL configuration"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.weather.views import WeatherForecastViewSet, WeatherComparisonViewSet
from apps.cities.views import CityViewSet
from ..views import api_root, health_check

router = DefaultRouter()
router.register(r"weather/forecasts", WeatherForecastViewSet, basename="forecast")
router.register(r"weather/comparisons", WeatherComparisonViewSet, basename="comparison")
router.register(r"cities", CityViewSet, basename="city")

urlpatterns = [
    path("", api_root, name="api-root"),
    path("health/", health_check, name="health-check"),
    path("", include(router.urls)),
]
