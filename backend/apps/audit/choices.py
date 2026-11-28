"""Enumeraciones y choices para el módulo auditoría."""

from django.db import models


class AccionAuditoria(models.TextChoices):
    INSERT = "INSERT", "Creación (INSERT)"
    UPDATE = "UPDATE", "Modificación (UPDATE)"
    DELETE = "DELETE", "Eliminación (DELETE)"
    LOGIN = "LOGIN", "Inicio de sesión (LOGIN)"
    APROBACION = "APROBACION", "Aprobación (APROBACION)"
    DENEGADO = "DENEGADO", "Acceso denegado (DENEGADO)"


class TipoMovimientoStock(models.TextChoices):
    ENTRADA = "ENTRADA", "Entrada"
    SALIDA = "SALIDA", "Salida"
    AJUSTE = "AJUSTE", "Ajuste de inventario"
    TRANSFERENCIA = "TRANSFERENCIA", "Transferencia entre locales"
