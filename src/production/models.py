from django.db import models
from core.common.models import Auditable


class Maquina(Auditable):
    nombre = models.CharField(max_length=100)
    local = models.ForeignKey("identity.Local", on_delete=models.PROTECT, related_name="maquinas")
    tipo_maquina = models.CharField(max_length=50, help_text="impresora, plancha, maquina_coser, plotter")
    estado = models.CharField(max_length=30, default="operativa")

    class Meta:
        db_table = "production_maquina"
        verbose_name = "Máquina"
        verbose_name_plural = "Máquinas"

    def __str__(self):
        return f"{self.nombre} ({self.local.codigo})"


class OrdenProduccion(Auditable):
    class Estado(models.TextChoices):
        PLANIFICADA = "planificada", "Planificada"
        EN_PROCESO = "en_proceso", "En Proceso"
        TERMINADA = "terminada", "Terminada"
        ANULADA = "anulada", "Anulada"

    codigo_orden = models.CharField(max_length=50, unique=True)
    pedido_origen_id = models.IntegerField(null=True, blank=True, help_text="ID del pedido de venta si fue originada por venta")
    estado = models.CharField(max_length=30, choices=Estado.choices, default=Estado.PLANIFICADA)
    diseno = models.ForeignKey("catalog.Diseno", on_delete=models.SET_NULL, null=True, blank=True)
    fecha_limite = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "production_orden_produccion"
        indexes = [
            models.Index(fields=["estado", "creado_en"]),
        ]
        verbose_name = "Orden de Producción"
        verbose_name_plural = "Órdenes de Producción"

    def __str__(self):
        return f"{self.codigo_orden} - {self.get_estado_display()}"


class PasoProduccion(Auditable):
    class TipoPaso(models.TextChoices):
        DISENO = "diseno", "Diseño"
        IMPRESION = "impresion", "Impresión"
        CORTE = "corte", "Corte"
        PLANCHADO = "planchado", "Planchado"
        CONFECCION = "confeccion", "Confección"

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        EN_PROCESO = "en_proceso", "En Proceso"
        TERMINADO = "terminado", "Terminado"

    orden = models.ForeignKey(OrdenProduccion, on_delete=models.CASCADE, related_name="pasos")
    orden_paso = models.IntegerField(help_text="Secuencia del paso: 1, 2, 3...")
    tipo_paso = models.CharField(max_length=30, choices=TipoPaso.choices)
    local = models.ForeignKey("identity.Local", on_delete=models.PROTECT, related_name="pasos_produccion")
    estado = models.CharField(max_length=30, choices=Estado.choices, default=Estado.PENDIENTE)
    iniciado_en = models.DateTimeField(null=True, blank=True)
    terminado_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "production_paso_produccion"
        ordering = ["orden", "orden_paso"]
        verbose_name = "Paso de Producción"
        verbose_name_plural = "Pasos de Producción"

    def __str__(self):
        return f"{self.orden.codigo_orden} - Paso {self.orden_paso}: {self.get_tipo_paso_display()} en {self.local.codigo}"


class ConsumoMaterial(Auditable):
    class TipoConsumo(models.TextChoices):
        USO = "uso", "Uso Real"
        DESPERDICIO = "desperdicio", "Desperdicio"

    paso = models.ForeignKey(PasoProduccion, on_delete=models.CASCADE, related_name="consumos")
    partida = models.ForeignKey("inventory.Partida", on_delete=models.PROTECT, null=True, blank=True)
    um = models.CharField(max_length=20)
    cantidad_consumida = models.DecimalField(max_digits=12, decimal_places=4)
    tipo_consumo = models.CharField(max_length=20, choices=TipoConsumo.choices, default=TipoConsumo.USO)
    motivo_desperdicio = models.TextField(blank=True, default="")

    class Meta:
        db_table = "production_consumo_material"
        verbose_name = "Consumo de Material"
        verbose_name_plural = "Consumos de Material"

    def __str__(self):
        return f"{self.paso}: {self.cantidad_consumida} {self.um} ({self.get_tipo_consumo_display()})"


class OperacionMaquina(Auditable):
    paso = models.ForeignKey(PasoProduccion, on_delete=models.CASCADE, related_name="operaciones_maquina")
    maquina = models.ForeignKey(Maquina, on_delete=models.PROTECT)
    operador_trabajador_id = models.IntegerField(null=True, blank=True)
    duracion_minutos = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    resultado = models.CharField(max_length=50, blank=True, default="")
    nota = models.TextField(blank=True, default="")

    class Meta:
        db_table = "production_operacion_maquina"
        verbose_name = "Operación por Máquina"
        verbose_name_plural = "Operaciones por Máquina"

    def __str__(self):
        return f"{self.maquina.nombre} en {self.paso}"
