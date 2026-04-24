"""Cities app URL configuration"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CityViewSet

router = DefaultRouter()
router.register(r"", CityViewSet, basename="city")

app_name = "cities"

urlpatterns = [
    path("", include(router.urls)),
]
