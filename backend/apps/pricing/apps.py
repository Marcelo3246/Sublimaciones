"""Configuración de la app precios."""

from django.apps import AppConfig


class PricingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.apps.pricing"
    verbose_name = "Precios"
