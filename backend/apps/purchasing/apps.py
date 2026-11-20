"""Configuración de la app compras."""

from django.apps import AppConfig


class PurchasingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.apps.purchasing"
    verbose_name = "Compras"
