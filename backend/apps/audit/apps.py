"""Configuración de la app auditoría."""

from django.apps import AppConfig


class AuditConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.apps.audit"
    verbose_name = "Auditoría"
