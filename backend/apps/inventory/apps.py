"""Configuración de la app inventario."""

from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.apps.inventory"
    verbose_name = "Inventario"
