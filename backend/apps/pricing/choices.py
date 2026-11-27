"""Enumeraciones y choices para el módulo precios."""

from django.db import models


class Moneda(models.TextChoices):
    """Monedas admitidas para precios (mismos valores que inventory)."""

    USD = "USD", "Dólar estadounidense"
    VES = "VES", "Bolívar venezolano"
