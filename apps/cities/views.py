"""Cities app views"""
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import City
from .serializers import CitySerializer
import logging

logger = logging.getLogger(__name__)


class CityViewSet(viewsets.ModelViewSet):
    """ViewSet for City management"""

    queryset = City.objects.prefetch_related("aliases")
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["country", "is_capital", "timezone"]
    search_fields = ["name", "country"]
    ordering_fields = ["name", "population"]
    ordering = ["name"]
    pagination_class = None  # Disable pagination for cities

    def get_queryset(self):
        """Filter based on query parameters"""
        queryset = super().get_queryset()

        # Search by name or alias
        search = self.request.query_params.get("search", None)
        if search:
            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(aliases__alias__icontains=search)

        # Filter by is_capital
        is_capital = self.request.query_params.get("is_capital", None)
        if is_capital is not None:
            queryset = queryset.filter(is_capital=is_capital.lower() == "true")

        return queryset.distinct()
