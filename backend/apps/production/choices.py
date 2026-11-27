"""Enumeraciones y choices para el módulo producción."""

from django.db import models


class Moneda(models.TextChoices):
    """Monedas admitidas para costos de producción."""

    USD = "USD", "Dólar estadounidense"
    VES = "VES", "Bolívar venezolano"


class EstadoOrdenProduccion(models.TextChoices):
    """Ciclo de vida de una orden de producción (docs/ddl/06b.6-produccion.md)."""

    CREADA = "CREADA", "Creada"
    EN_PRODUCCION = "EN_PRODUCCION", "En producción"
    TERMINADA = "TERMINADA", "Terminada"
    ANULADA = "ANULADA", "Anulada"


class EstadoPasoProduccion(models.TextChoices):
    """Estado de un paso de la ruta multi-local (RF-31)."""

    PENDIENTE = "PENDIENTE", "Pendiente"
    EN_PROCESO = "EN_PROCESO", "En proceso"
    TERMINADO = "TERMINADO", "Terminado"


class TipoPaso(models.TextChoices):
    """Tipos de tarea de la ruta de producción."""

    IMPRESION = "IMPRESION", "Impresión"
    CORTE = "CORTE", "Corte"
    PLANCHADO = "PLANCHADO", "Planchado"
    CONFECCION = "CONFECCION", "Confección"
    DISENO = "DISENO", "Diseño"


class TipoMaquina(models.TextChoices):
    """Categorías de máquina del parque de equipos."""

    IMPRESORA = "IMPRESORA", "Impresora"
    PLANCHA = "PLANCHA", "Plancha"
    CORTADORA = "CORTADORA", "Cortadora"
    OTRO = "OTRO", "Otro"


class EstadoMaquina(models.TextChoices):
    """Estado operativo de una máquina."""

    OPERATIVA = "OPERATIVA", "Operativa"
    MANTENIMIENTO = "MANTENIMIENTO", "En mantenimiento"
    INACTIVA = "INACTIVA", "Inactiva"


class TipoConsumo(models.TextChoices):
    """Consumo útil frente a desperdicio (RF-34)."""

    USO = "USO", "Uso"
    DESPERDICIO = "DESPERDICIO", "Desperdicio"


class ResultadoOperacion(models.TextChoices):
    """Resultado de una operación de máquina (RF-33)."""

    COMPLETADO = "COMPLETADO", "Completado"
    DEFECTUOSO = "DEFECTUOSO", "Defectuoso"
    PARCIAL = "PARCIAL", "Parcial"
