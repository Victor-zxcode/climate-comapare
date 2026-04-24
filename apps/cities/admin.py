"""Cities app admin configuration"""
from django.contrib import admin
from .models import City, CityAlias


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "is_capital", "latitude", "longitude", "timezone")
    list_filter = ("is_capital", "country")
    search_fields = ("name", "country")
    readonly_fields = ("created_at", "updated_at", "last_weather_update")

    fieldsets = (
        ("Basic Information", {"fields": ("name", "country", "state")}),
        ("Geographic Data", {"fields": ("latitude", "longitude", "timezone")}),
        ("Additional Info", {"fields": ("population", "is_capital")}),
        ("Metadata", {"fields": ("created_at", "updated_at", "last_weather_update")}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return self.readonly_fields + ("latitude", "longitude")
        return self.readonly_fields


@admin.register(CityAlias)
class CityAliasAdmin(admin.ModelAdmin):
    list_display = ("alias", "city")
    search_fields = ("alias", "city__name")
    list_filter = ("city__country",)
