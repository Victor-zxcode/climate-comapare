"""Weather app URL configuration"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherForecastViewSet, WeatherComparisonViewSet

router = DefaultRouter()
router.register(r"forecasts", WeatherForecastViewSet, basename="forecast")
router.register(r"comparisons", WeatherComparisonViewSet, basename="comparison")

app_name = "weather"

urlpatterns = [
    path("", include(router.urls)),
]
