"""Configuración de la app ventas."""

from django.apps import AppConfig


class SalesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.apps.sales"
    verbose_name = "Ventas"
