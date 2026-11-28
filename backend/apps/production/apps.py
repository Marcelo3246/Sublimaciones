"""Configuración de la app producción."""

from django.apps import AppConfig


class ProductionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.apps.production"
    verbose_name = "Producción"
