"""Enumeraciones y choices para el módulo ventas."""

from django.db import models

from backend.apps.pricing.choices import Moneda  # noqa: F401  (re-exportada)


class EstadoPedido(models.TextChoices):
    """Línea de producción por estados del pedido (RF-37)."""

    COTIZADO = "COTIZADO", "Cotizado"
    CONFIRMADO = "CONFIRMADO", "Confirmado"
    EN_PRODUCCION = "EN_PRODUCCION", "En producción"
    LISTO = "LISTO", "Listo"
    ENTREGADO = "ENTREGADO", "Entregado"
    FACTURADO = "FACTURADO", "Facturado"
    ANULADO = "ANULADO", "Anulado"


class TipoLineaPedido(models.TextChoices):
    """Discriminador de la línea de pedido."""

    PRODUCTO = "PRODUCTO", "Producto"
    PRODUCTO_PERSONALIZADO = "PRODUCTO_PERSONALIZADO", "Producto personalizado"
    SERVICIO_PURO = "SERVICIO_PURO", "Servicio puro"


class MetodoCobro(models.TextChoices):
    """Tipo de pago del cobro (RF-42)."""

    EFECTIVO = "EFECTIVO", "Efectivo"
    PUNTO = "PUNTO", "Punto de venta"
    TRANSFERENCIA = "TRANSFERENCIA", "Transferencia"
    DIVISA = "DIVISA", "Divisa"


class TipoFactura(models.TextChoices):
    """Tipo de factura emitida."""

    PROPIA = "PROPIA", "Propia"
    FISCAL = "FISCAL", "Fiscal"


class EstadoFactura(models.TextChoices):
    """Estado de la factura."""

    EMITIDA = "EMITIDA", "Emitida"
    ANULADA = "ANULADA", "Anulada"
