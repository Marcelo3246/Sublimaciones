"""Modelos de datos del módulo producción multi-local.

Implementa el parque de máquinas, órdenes de producción con ruta
multi-local por pasos, consumo de material por medición y operaciones
de máquina con class Meta y db_table explícito
(ver docs/tasks/tareas-grupo-base-de-datos.md).

Semántica: docs/modelo-datos/06.6-produccion.md y
docs/ddl/06b.6-produccion.md (RF-30 a RF-35).
"""

from django.db import models

from backend.apps.production.choices import (
    EstadoMaquina,
    EstadoOrdenProduccion,
    EstadoPasoProduccion,
    Moneda,
    ResultadoOperacion,
    TipoConsumo,
    TipoMaquina,
    TipoPaso,
)
from backend.common.base_models import ActivoMixin, TimeStampedModel


class Maquina(TimeStampedModel, ActivoMixin):
    """Catálogo de equipos de un local (plóteres, planchas, costura)."""

    codigo = models.CharField("código", max_length=30, unique=True)
    nombre = models.CharField("nombre", max_length=100)
    local = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        related_name="maquinas",
        verbose_name="local",
    )
    tipo = models.CharField(
        "tipo",
        max_length=20,
        choices=TipoMaquina.choices,
        default=TipoMaquina.OTRO,
    )
    estado = models.CharField(
        "estado",
        max_length=20,
        choices=EstadoMaquina.choices,
        default=EstadoMaquina.OPERATIVA,
    )
    horas_operativas = models.DecimalField(
        "horas operativas",
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    class Meta:
        verbose_name = "máquina"
        verbose_name_plural = "máquinas"
        db_table = "produccion.maquina"
        ordering = ["local", "codigo"]
        indexes = [
            models.Index(
                fields=["local"],
                name="production_maquina_local_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(tipo__in=TipoMaquina.values),
                name="production_maquina_tipo_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(estado__in=EstadoMaquina.values),
                name="production_maquina_estado_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(horas_operativas__gte=0),
                name="production_maquina_horas_ck",
            ),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nombre} ({self.local.codigo})"


class OrdenProduccion(TimeStampedModel, ActivoMixin):
    """Orden de producción con producto, cantidad y local de origen (RF-30)."""

    codigo = models.CharField("código", max_length=30, unique=True)
    pedido_venta_id = models.IntegerField(
        "pedido de venta",
        null=True,
        blank=True,
        help_text="Referencia débil a ventas.pedido_venta; vacío si es fabricación directa",
    )
    variante = models.ForeignKey(
        "catalog.VarianteProducto",
        on_delete=models.PROTECT,
        related_name="ordenes_produccion",
        verbose_name="variante",
    )
    cantidad = models.DecimalField(
        "cantidad", max_digits=12, decimal_places=4
    )
    local_origen = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        related_name="ordenes_produccion",
        verbose_name="local de origen",
    )
    estado = models.CharField(
        "estado",
        max_length=20,
        choices=EstadoOrdenProduccion.choices,
        default=EstadoOrdenProduccion.CREADA,
    )
    fecha_limite = models.DateField("fecha límite", null=True, blank=True)
    costo_materiales = models.DecimalField(
        "costo de materiales",
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )
    costo_horas = models.DecimalField(
        "costo de horas", max_digits=14, decimal_places=2, null=True, blank=True
    )
    costo_total = models.DecimalField(
        "costo total", max_digits=14, decimal_places=2, null=True, blank=True
    )
    moneda = models.CharField(
        "moneda", max_length=3, choices=Moneda.choices, default=Moneda.USD
    )
    fecha_cierre = models.DateTimeField(
        "fecha de cierre", null=True, blank=True
    )

    class Meta:
        verbose_name = "orden de producción"
        verbose_name_plural = "órdenes de producción"
        db_table = "produccion.orden_produccion"
        ordering = ["-creado_en"]
        indexes = [
            models.Index(
                fields=["estado", "local_origen"],
                name="production_oc_estado_idx",
            ),
            models.Index(
                fields=["pedido_venta_id"],
                name="production_oc_pedido_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad__gt=0),
                name="production_oc_cantidad_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(estado__in=EstadoOrdenProduccion.values),
                name="production_oc_estado_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(moneda__in=Moneda.values),
                name="production_oc_moneda_ck",
            ),
            # RF-35: para cerrar, exige costo total y fecha de cierre
            models.CheckConstraint(
                condition=(
                    ~models.Q(estado=EstadoOrdenProduccion.TERMINADA)
                    | models.Q(costo_total__isnull=False, fecha_cierre__isnull=False)
                ),
                name="production_oc_cierre_ck",
            ),
        ]

    def __str__(self):
        return f"{self.codigo} ({self.get_estado_display()})"


class PasoProduccion(TimeStampedModel, ActivoMixin):
    """Paso de la ruta multi-local: un tramo encadenado en un local (RF-31)."""

    orden_produccion = models.ForeignKey(
        OrdenProduccion,
        on_delete=models.CASCADE,
        related_name="pasos",
        verbose_name="orden de producción",
    )
    orden_paso = models.PositiveSmallIntegerField("orden del paso")
    tipo = models.CharField(
        "tipo de paso",
        max_length=20,
        choices=TipoPaso.choices,
        default=TipoPaso.IMPRESION,
    )
    local = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        related_name="pasos_produccion",
        verbose_name="local de ejecución",
    )
    trabajador = models.ForeignKey(
        "hr.Trabajador",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="pasos_produccion",
        verbose_name="trabajador",
        help_text="Trabajador asignado al paso; vacío hasta asignar",
    )
    descripcion_tarea = models.CharField(
        "descripción de la tarea", max_length=300, blank=True, default=""
    )
    estado = models.CharField(
        "estado",
        max_length=20,
        choices=EstadoPasoProduccion.choices,
        default=EstadoPasoProduccion.PENDIENTE,
    )
    iniciado_en = models.DateTimeField(
        "iniciado en", null=True, blank=True
    )
    terminado_en = models.DateTimeField(
        "terminado en", null=True, blank=True
    )

    class Meta:
        verbose_name = "paso de producción"
        verbose_name_plural = "pasos de producción"
        db_table = "produccion.paso_produccion"
        ordering = ["orden_paso"]
        indexes = [
            models.Index(
                fields=["local", "estado"],
                name="production_paso_loc_est_idx",
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["orden_produccion", "orden_paso"],
                name="production_paso_orden_uk",
            ),
            models.CheckConstraint(
                condition=models.Q(orden_paso__gt=0),
                name="production_paso_orden_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(estado__in=EstadoPasoProduccion.values),
                name="production_paso_estado_ck",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(iniciado_en__isnull=True)
                    | models.Q(terminado_en__isnull=True)
                    | models.Q(iniciado_en__lte=models.F("terminado_en"))
                ),
                name="production_paso_fechas_ck",
            ),
        ]

    def __str__(self):
        return f"Paso {self.orden_paso} {self.get_tipo_display()} - {self.orden_produccion.codigo}"


class ConsumoMaterial(TimeStampedModel, ActivoMixin):
    """Salida de material de un paso sobre lote o stock (RF-32, RF-34)."""

    paso = models.ForeignKey(
        PasoProduccion,
        on_delete=models.CASCADE,
        related_name="consumos",
        verbose_name="paso",
    )
    lote = models.ForeignKey(
        "inventory.Lote",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="consumos_produccion",
        verbose_name="lote",
        help_text="Lote físico para materiales continuos",
    )
    stock = models.ForeignKey(
        "inventory.Stock",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="consumos_produccion",
        verbose_name="stock",
        help_text="Saldo contable cuando no aplica lote",
    )
    cantidad_consumida = models.DecimalField(
        "cantidad consumida", max_digits=12, decimal_places=4
    )
    unidad_medida = models.ForeignKey(
        "catalog.UnidadMedida",
        on_delete=models.PROTECT,
        related_name="consumos_produccion",
        verbose_name="unidad de medida",
    )
    tipo = models.CharField(
        "tipo de consumo",
        max_length=20,
        choices=TipoConsumo.choices,
        default=TipoConsumo.USO,
    )
    motivo_desperdicio = models.CharField(
        "motivo de desperdicio",
        max_length=200,
        blank=True,
        default="",
        help_text="Obligatorio cuando el consumo es desperdicio (RF-34)",
    )
    movimiento_stock_id = models.IntegerField(
        "movimiento de stock",
        null=True,
        blank=True,
        help_text="Referencia débil a inventory.movimiento_stock como traza",
    )

    class Meta:
        verbose_name = "consumo de material"
        verbose_name_plural = "consumos de material"
        db_table = "produccion.consumo_material"
        ordering = ["id"]
        indexes = [
            models.Index(
                fields=["paso"],
                name="production_consumo_paso_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad_consumida__gt=0),
                name="production_consumo_cantidad_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(tipo__in=TipoConsumo.values),
                name="production_consumo_tipo_ck",
            ),
            # XOR: exactamente uno entre lote y stock
            models.CheckConstraint(
                condition=(
                    models.Q(lote__isnull=False, stock__isnull=True)
                    | models.Q(lote__isnull=True, stock__isnull=False)
                ),
                name="production_consumo_excluyente",
            ),
            models.CheckConstraint(
                condition=(
                    ~models.Q(tipo=TipoConsumo.DESPERDICIO)
                    | models.Q(motivo_desperdicio__gt="")
                ),
                name="production_consumo_motivo_ck",
            ),
        ]

    def __str__(self):
        origen = self.lote if self.lote_id else self.stock
        return f"{self.tipo}: {self.cantidad_consumida} en paso {self.paso_id} ({origen})"


class OperacionMaquina(TimeStampedModel, ActivoMixin):
    """Registro de uso de máquina en un paso (RF-33)."""

    paso = models.ForeignKey(
        PasoProduccion,
        on_delete=models.CASCADE,
        related_name="operaciones_maquina",
        verbose_name="paso",
    )
    maquina = models.ForeignKey(
        Maquina,
        on_delete=models.PROTECT,
        related_name="operaciones",
        verbose_name="máquina",
    )
    operador_trabajador = models.ForeignKey(
        "hr.Trabajador",
        on_delete=models.PROTECT,
        related_name="operaciones_maquina",
        verbose_name="operador",
    )
    duracion_minutos = models.DecimalField(
        "duración (minutos)", max_digits=8, decimal_places=2
    )
    resultado = models.CharField(
        "resultado",
        max_length=20,
        choices=ResultadoOperacion.choices,
        default=ResultadoOperacion.COMPLETADO,
    )
    nota = models.CharField("nota", max_length=300, blank=True, default="")

    class Meta:
        verbose_name = "operación de máquina"
        verbose_name_plural = "operaciones de máquina"
        db_table = "produccion.operacion_maquina"
        ordering = ["-creado_en"]
        indexes = [
            models.Index(
                fields=["maquina", "-creado_en"],
                name="production_op_maquina_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(duracion_minutos__gte=0),
                name="production_op_duracion_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(resultado__in=ResultadoOperacion.values),
                name="production_op_resultado_ck",
            ),
        ]

    def __str__(self):
        return f"{self.maquina} - {self.get_resultado_display()} ({self.duracion_minutos} min)"
