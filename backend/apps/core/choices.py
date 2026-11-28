"""Enumeraciones y choices para el núcleo del sistema."""

from django.db import models


class RolUsuario(models.TextChoices):
    ADMINISTRADOR = "admin", "Administrador"
    GERENTE = "gerente", "Gerente de local"
    OPERARIO = "operario", "Operario de producción"
    VENDEDOR = "vendedor", "Vendedor / Cajero"


class TipoComprobante(models.TextChoices):
    FACTURA = "factura", "Factura"
    NOTA_ENTREGA = "nota_entrega", "Nota de entrega"
    ORDEN_PRODUCCION = "orden_produccion", "Orden de producción"
    PRESUPUESTO = "presupuesto", "Presupuesto comercial"
    PLANILLA_TRANSFERENCIA = "planilla_transferencia", "Planilla de transferencia"
    ACTA_DESPERDICIO = "acta_desperdicio", "Acta de desperdicio"
    COMPROBANTE_COMISION = "comprobante_comision", "Comprobante de comisión"
