"""
Django settings for development environment
"""
from .base import *

DEBUG = True

# Development security - disable for development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Development apps
INSTALLED_APPS += [
    "django_extensions",
]

if DEBUG:
    MIDDLEWARE += ["django_debug_toolbar.middleware.DebugToolbarMiddleware"]
    INSTALLED_APPS += ["debug_toolbar"]

# Development databases
DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": BASE_DIR / env("DB_NAME", default="db.sqlite3"),
    }
}

# Verbose logging in development
LOGGING["loggers"]["django"]["level"] = "DEBUG"

# Email backend - Console output in development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# CORS settings - Allow all in development
CORS_ALLOW_ALL_ORIGINS = True

print("✅ Using Development Settings")
