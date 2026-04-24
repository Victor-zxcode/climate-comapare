"""Constants used across the application"""

# Weather conditions
WEATHER_CONDITIONS = {
    0: "Céu limpo",
    1: "Parcialmente nublado",
    2: "Nublado",
    3: "Encoberto",
    45: "Nevoeiro",
    48: "Nevoeiro com deposição de gelo",
    51: "Chuvisco leve",
    53: "Chuvisco moderado",
    55: "Chuvisco denso",
    61: "Chuva leve",
    63: "Chuva moderada",
    65: "Chuva forte",
    71: "Neve leve",
    73: "Neve moderada",
    75: "Neve forte",
    77: "Grãos de neve",
    80: "Pancadas de chuva leve",
    81: "Pancadas de chuva moderada",
    82: "Pancadas de chuva forte",
    85: "Pancadas de neve leve",
    86: "Pancadas de neve forte",
    95: "Tempestade com raios leves",
    96: "Tempestade com raios moderados",
    99: "Tempestade com raios fortes",
}

# Cardinal directions
CARDINAL_DIRECTIONS = [
    "N",
    "NNE",
    "NE",
    "ENE",
    "E",
    "ESE",
    "SE",
    "SSE",
    "S",
    "SSW",
    "SW",
    "WSW",
    "W",
    "WNW",
    "NW",
    "NNW",
]

# API Timeouts (seconds)
OPEN_METEO_TIMEOUT = 10
GEOCODING_TIMEOUT = 10

# Max cities for comparison
MAX_CITIES_COMPARISON = 5

# Cache timeout (seconds)
CACHE_TIMEOUT_SHORT = 300  # 5 minutes
CACHE_TIMEOUT_MEDIUM = 1800  # 30 minutes
CACHE_TIMEOUT_LONG = 3600  # 1 hour

# Pagination
DEFAULT_PAGE_SIZE = 100
