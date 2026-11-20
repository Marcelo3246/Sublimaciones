"""Enumeraciones y choices para el módulo inventario."""

from django.db import models


class TipoMovimiento(models.TextChoices):
    """Tipo de movimiento de stock admitido en el inventario."""

    ENTRADA = "ENTRADA", "Entrada"
    SALIDA = "SALIDA", "Salida"
    TRANSFERENCIA = "TRANSFERENCIA", "Transferencia entre locales"


class EstadoGuiaTransferencia(models.TextChoices):
    """Ciclo de vida de una guía de transferencia entre locales."""

    BORRADOR = "BORRADOR", "Borrador"
    EN_TRANSITO = "EN_TRANSITO", "En tránsito"
    RECIBIDA = "RECIBIDA", "Recibida"
    RECHAZADA = "RECHAZADA", "Rechazada"


class EstadoLineaGuia(models.TextChoices):
    """Estado de una línea dentro de una guía de transferencia."""

    PENDIENTE = "PENDIENTE", "Pendiente"
    DESPACHADA = "DESPACHADA", "Despachada"
    RECIBIDA = "RECIBIDA", "Recibida"
    DESVIADA = "DESVIADA", "Desviada"


class Moneda(models.TextChoices):
    """Monedas admitidas para montos de inventario."""

    USD = "USD", "Dólar estadounidense"
    VES = "VES", "Bolívar venezolano"
