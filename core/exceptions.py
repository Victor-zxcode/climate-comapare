"""Custom exceptions"""


class ClimateCompareException(Exception):
    """Base exception for Climate Compare"""

    pass


class APIException(ClimateCompareException):
    """Exception for API-related errors"""

    pass


class OpenMeteoAPIException(APIException):
    """Exception for Open-Meteo API errors"""

    pass


class GeocodingException(APIException):
    """Exception for geocoding errors"""

    pass


class ValidationException(ClimateCompareException):
    """Exception for validation errors"""

    pass


class DataProcessingException(ClimateCompareException):
    """Exception for data processing errors"""

    pass
