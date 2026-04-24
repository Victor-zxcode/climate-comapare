"""API root views"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def api_root(request):
    """API root endpoint with version info"""
    return Response(
        {
            "api_version": "v1",
            "endpoints": {
                "weather": request.build_absolute_uri("/api/v1/weather/"),
                "cities": request.build_absolute_uri("/api/v1/cities/"),
            },
            "documentation": "https://github.com/seu-usuario/climate-compare/wiki/API",
        }
    )


@api_view(["GET"])
def health_check(request):
    """Health check endpoint"""
    return Response(
        {
            "status": "healthy",
            "message": "Climate Compare API is running",
        },
        status=status.HTTP_200_OK,
    )
