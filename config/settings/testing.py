"""
Django settings for testing environment
"""
from .base import *

DEBUG = True

# Use simple in-memory password hasher for faster tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Use in-memory database for testing
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Disable migrations for tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# Email backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# CORS
CORS_ALLOW_ALL_ORIGINS = True

print("🧪 Using Testing Settings")
