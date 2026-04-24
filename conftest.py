"""
Pytest configuration file
"""
import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.testing")

django.setup()

# Pytest configuration
def pytest_configure():
    """Configure pytest"""
    pass


# Fixtures
import pytest
from django.test import Client


@pytest.fixture
def client():
    """Return a Django test client"""
    return Client()


@pytest.fixture
def django_db_setup(django_db_setup, django_db_blocker):
    """Setup Django database for tests"""
    with django_db_blocker.unblock():
        pass
