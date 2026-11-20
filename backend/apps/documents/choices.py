"""Enumeraciones y choices para el módulo documentos."""

from django.db import models


class TipoDocumento(models.TextChoices):
    FACTURA = "factura", "Factura"
    NOTA_ENTREGA = "nota_entrega", "Nota de entrega"
    ORDEN_PRODUCCION = "orden_produccion", "Orden de producción"
    PRESUPUESTO = "presupuesto", "Presupuesto comercial"
    PLANILLA_TRANSFERENCIA = "planilla_transferencia", "Planilla de transferencia"
    ACTA_DESPERDICIO = "acta_desperdicio", "Acta de desperdicio"
    COMPROBANTE_COMISION = "comprobante_comision", "Comprobante de comisión"


class EstadoDocumento(models.TextChoices):
    GENERADO = "generado", "Generado"
    ANULADO = "anulado", "Anulado"
