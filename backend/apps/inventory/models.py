"""Modelos de datos del inventario multi-local.

Implementa stock por local, lotes trazables, movimientos, guías de
transferencia y niveles mínimos con class Meta y db_table explícito
(ver tasks/tareas-grupo-base-de-datos.md).
"""

from django.db import models
from django.utils import timezone

from backend.apps.inventory.choices import (
    EstadoGuiaTransferencia,
    EstadoLineaGuia,
    Moneda,
    TipoMovimiento,
)
from backend.common.base_models import ActivoMixin, TimeStampedModel


class Stock(TimeStampedModel, ActivoMixin):
    """Saldo agregado de material o variante en un local (XOR)."""

    local = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        related_name="stocks",
        verbose_name="local",
    )
    variante = models.ForeignKey(
        "catalog.VarianteProducto",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="stocks",
        verbose_name="variante",
    )
    material = models.ForeignKey(
        "catalog.Material",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="stocks",
        verbose_name="material",
    )
    cantidad_disponible = models.DecimalField(
        "cantidad disponible",
        max_digits=12,
        decimal_places=4,
        default=0,
    )
    cantidad_reservada = models.DecimalField(
        "cantidad reservada",
        max_digits=12,
        decimal_places=4,
        default=0,
    )

    class Meta:
        verbose_name = "stock"
        verbose_name_plural = "stocks"
        db_table = "inventario.stock"
        ordering = ["-actualizado_en"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(material__isnull=False, variante__isnull=True)
                    | models.Q(material__isnull=True, variante__isnull=False)
                ),
                name="inventory_stock_excluyente",
            ),
            models.CheckConstraint(
                condition=models.Q(cantidad_disponible__gte=0),
                name="inventory_stock_disponible_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(cantidad_reservada__gte=0),
                name="inventory_stock_reservada_ck",
            ),
            models.UniqueConstraint(
                fields=["local", "material"],
                condition=models.Q(material__isnull=False),
                name="inventory_stock_material_uk",
            ),
            models.UniqueConstraint(
                fields=["local", "variante"],
                condition=models.Q(variante__isnull=False),
                name="inventory_stock_variante_uk",
            ),
        ]

    def __str__(self):
        item = self.variante if self.variante_id else self.material
        return f"{self.local.codigo} - {item} ({self.cantidad_disponible})"


class Lote(TimeStampedModel, ActivoMixin):
    """Lote físico trazable de un material (rollos, insumos)."""

    material = models.ForeignKey(
        "catalog.Material",
        on_delete=models.PROTECT,
        related_name="lotes",
        verbose_name="material",
    )
    local = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        related_name="lotes",
        verbose_name="local",
    )
    numero_lote = models.CharField("número de lote", max_length=30)
    longitud_inicial = models.DecimalField(
        "longitud inicial",
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Longitud de ingreso para materiales continuos (rollos)",
    )
    longitud_actual = models.DecimalField(
        "longitud actual",
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Saldo físico remanente del lote",
    )
    costo_unitario = models.DecimalField(
        "costo unitario",
        max_digits=14,
        decimal_places=2,
    )
    moneda = models.CharField(
        "moneda",
        max_length=3,
        choices=Moneda.choices,
        default=Moneda.USD,
    )
    fecha_ingreso = models.DateField("fecha de ingreso", default=timezone.now)
    fecha_vencimiento = models.DateField(
        "fecha de vencimiento",
        null=True,
        blank=True,
        help_text="Vigencia del lote; vacío si no caduca",
    )

    class Meta:
        verbose_name = "lote"
        verbose_name_plural = "lotes"
        db_table = "inventario.lote"
        ordering = ["-fecha_ingreso", "numero_lote"]
        indexes = [
            models.Index(
                fields=["local", "material"],
                name="inventory_lote_loc_mat_idx",
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["numero_lote"],
                name="inventory_lote_numero_uk",
            ),
            models.CheckConstraint(
                condition=models.Q(costo_unitario__gte=0),
                name="inventory_lote_costo_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(moneda__in=Moneda.values),
                name="inventory_lote_moneda_ck",
            ),
        ]

    def __str__(self):
        return f"{self.numero_lote} - {self.material.codigo}"


class MovimientoStock(TimeStampedModel, ActivoMixin):
    """Registro de entrada, salida o transferencia de stock en un local."""

    tipo = models.CharField(
        "tipo",
        max_length=20,
        choices=TipoMovimiento.choices,
        default=TipoMovimiento.ENTRADA,
    )
    local = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        related_name="movimientos_stock",
        verbose_name="local",
    )
    cantidad = models.DecimalField(
        "cantidad",
        max_digits=12,
        decimal_places=4,
    )
    referencia = models.CharField(
        "referencia",
        max_length=100,
        blank=True,
        default="",
        help_text="Documento u operación que originó el movimiento",
    )

    class Meta:
        verbose_name = "movimiento de stock"
        verbose_name_plural = "movimientos de stock"
        db_table = "inventario.movimiento_stock"
        ordering = ["-creado_en"]
        indexes = [
            models.Index(
                fields=["local", "-creado_en"],
                name="inventory_mov_loc_fecha_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad__gt=0),
                name="inventory_movimiento_cantidad_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(tipo__in=TipoMovimiento.values),
                name="inventory_movimiento_tipo_ck",
            ),
        ]

    def __str__(self):
        return f"{self.tipo} {self.cantidad} en {self.local.codigo}"


class GuiaTransferencia(TimeStampedModel, ActivoMixin):
    """Guía de transferencia de mercancía entre dos locales."""

    codigo_guia = models.CharField("código de guía", max_length=30)
    local_origen = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        related_name="guias_salida",
        verbose_name="local de origen",
    )
    local_destino = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        related_name="guias_entrada",
        verbose_name="local de destino",
    )
    estado = models.CharField(
        "estado",
        max_length=20,
        choices=EstadoGuiaTransferencia.choices,
        default=EstadoGuiaTransferencia.BORRADOR,
    )

    class Meta:
        verbose_name = "guía de transferencia"
        verbose_name_plural = "guías de transferencia"
        db_table = "inventario.guia_transferencia"
        ordering = ["-creado_en"]
        constraints = [
            models.UniqueConstraint(
                fields=["codigo_guia"],
                name="inventory_guia_codigo_uk",
            ),
            models.CheckConstraint(
                condition=~models.Q(local_origen=models.F("local_destino")),
                name="inventory_guia_locales_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(estado__in=EstadoGuiaTransferencia.values),
                name="inventory_guia_estado_ck",
            ),
        ]

    def __str__(self):
        return f"{self.codigo_guia} ({self.get_estado_display()})"


class LineaGuiaTransferencia(TimeStampedModel, ActivoMixin):
    """Ítem transportado por una guía: un lote o una variante (XOR)."""

    guia = models.ForeignKey(
        GuiaTransferencia,
        on_delete=models.CASCADE,
        related_name="lineas",
        verbose_name="guía",
    )
    lote = models.ForeignKey(
        Lote,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="lineas_guia",
        verbose_name="lote",
    )
    variante = models.ForeignKey(
        "catalog.VarianteProducto",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="lineas_guia",
        verbose_name="variante",
    )
    cantidad = models.DecimalField(
        "cantidad",
        max_digits=12,
        decimal_places=4,
    )
    unidad_medida = models.ForeignKey(
        "catalog.UnidadMedida",
        on_delete=models.PROTECT,
        related_name="lineas_guia",
        verbose_name="unidad de medida",
    )
    estado = models.CharField(
        "estado",
        max_length=20,
        choices=EstadoLineaGuia.choices,
        default=EstadoLineaGuia.PENDIENTE,
    )

    class Meta:
        verbose_name = "línea de guía"
        verbose_name_plural = "líneas de guía"
        db_table = "inventario.linea_guia_transferencia"
        ordering = ["creado_en"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(lote__isnull=False, variante__isnull=True)
                    | models.Q(lote__isnull=True, variante__isnull=False)
                ),
                name="inventory_linea_excluyente",
            ),
            models.CheckConstraint(
                condition=models.Q(cantidad__gt=0),
                name="inventory_linea_cantidad_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(estado__in=EstadoLineaGuia.values),
                name="inventory_linea_estado_ck",
            ),
        ]

    def __str__(self):
        item = self.lote if self.lote_id else self.variante
        return f"Línea de {self.guia.codigo_guia} - {item}"


class NivelMinimo(TimeStampedModel, ActivoMixin):
    """Alerta de stock mínimo por local para un material o producto (XOR)."""

    local = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        related_name="niveles_minimos",
        verbose_name="local",
    )
    producto = models.ForeignKey(
        "catalog.Producto",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="niveles_minimos",
        verbose_name="producto",
    )
    material = models.ForeignKey(
        "catalog.Material",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="niveles_minimos",
        verbose_name="material",
    )
    cantidad_minima_alerta = models.DecimalField(
        "cantidad mínima de alerta",
        max_digits=12,
        decimal_places=4,
    )

    class Meta:
        verbose_name = "nivel mínimo"
        verbose_name_plural = "niveles mínimos"
        db_table = "inventario.nivel_minimo"
        ordering = ["local"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(material__isnull=False, producto__isnull=True)
                    | models.Q(material__isnull=True, producto__isnull=False)
                ),
                name="inventory_nivel_excluyente",
            ),
            models.CheckConstraint(
                condition=models.Q(cantidad_minima_alerta__gte=0),
                name="inventory_nivel_cantidad_ck",
            ),
            models.UniqueConstraint(
                fields=["local", "material"],
                condition=models.Q(material__isnull=False),
                name="inventory_nivel_material_uk",
            ),
            models.UniqueConstraint(
                fields=["local", "producto"],
                condition=models.Q(producto__isnull=False),
                name="inventory_nivel_producto_uk",
            ),
        ]

    def __str__(self):
        item = self.producto if self.producto_id else self.material
        return f"{self.local.codigo} - {item}: {self.cantidad_minima_alerta}"
