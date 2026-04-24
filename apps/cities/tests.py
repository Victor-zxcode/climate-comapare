"""Cities app tests"""
from django.test import TestCase
from .models import City


class CityTestCase(TestCase):
    def setUp(self):
        self.city = City.objects.create(
            name="Brasília",
            country="Brasil",
            latitude=-15.78,
            longitude=-47.89,
            timezone="America/Sao_Paulo",
            is_capital=True,
        )

    def test_city_creation(self):
        self.assertEqual(self.city.name, "Brasília")
        self.assertEqual(self.city.country, "Brasil")
        self.assertTrue(self.city.is_capital)

    def test_full_location(self):
        self.assertIn("Brasília", self.city.full_location)
        self.assertIn("Brasil", self.city.full_location)
