"""Enumeraciones y choices para el módulo compras."""

from django.db import models


class Moneda(models.TextChoices):
    """Monedas admitidas para montos de compra."""

    USD = "USD", "Dólar estadounidense"
    VES = "VES", "Bolívar venezolano"


class EstadoOrdenCompra(models.TextChoices):
    """Ciclo de vida de una orden de compra (docs/ddl/06b.5-compras.md)."""

    BORRADOR = "BORRADOR", "Borrador"
    ENVIADA = "ENVIADA", "Enviada"
    PARCIAL = "PARCIAL", "Recepción parcial"
    RECIBIDA = "RECIBIDA", "Recibida"
    CERRADA = "CERRADA", "Cerrada"
    ANULADA = "ANULADA", "Anulada"


class EstadoRecepcionCompra(models.TextChoices):
    """Estado de una recepción de mercancía contra una orden."""

    PENDIENTE = "PENDIENTE", "Pendiente"
    TOTAL = "TOTAL", "Recepción total"
    PARCIAL = "PARCIAL", "Recepción parcial"
    ANULADA = "ANULADA", "Anulada"
