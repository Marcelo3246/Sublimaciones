"""Modelos de datos para el módulo precios.

Implementa la matriz de precios, el historial de cambios de precio y los
parámetros de la fórmula con vigencia por fechas, con class Meta y
db_table explícito.

Fuente: RF-44 a RF-47 (docs/03-requerimientos-del-sistema.md),
docs/modelo-datos/06.8-precios.md y docs/ddl/06b.8-precios.md.

El precio final (``precio_base × margen × (1 + iva)``) se calcula en la capa
de servicios al cotizar y no se persiste como campo derivado (RF-44).
"""

from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q

from backend.apps.pricing.choices import Moneda
from backend.common.base_models import ActivoMixin, TimeStampedModel


class ItemMatrizPrecios(TimeStampedModel, ActivoMixin):
    """Precio base de un producto, variante o servicio (destinos excluyentes)."""

    producto = models.ForeignKey(
        "catalog.Producto",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="items_matriz_precios",
        verbose_name="producto",
    )
    variante = models.ForeignKey(
        "catalog.VarianteProducto",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="items_matriz_precios",
        verbose_name="variante",
    )
    servicio = models.ForeignKey(
        "catalog.Servicio",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="items_matriz_precios",
        verbose_name="servicio",
    )
    material = models.ForeignKey(
        "catalog.Material",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="items_matriz_precios",
        verbose_name="material condicionante",
        help_text="Material que condiciona el precio (p. ej. vinil blanco)",
    )
    unidad_medida = models.ForeignKey(
        "catalog.UnidadMedida",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="items_matriz_precios",
        verbose_name="unidad de medida",
        help_text="Unidad en la que se cotiza (pieza, metro...)",
    )
    medida_cantidad = models.DecimalField(
        "medida",
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Valor numérico de la medida (p. ej. 11 para una taza de 11 oz)",
    )
    unidad_medida_medida = models.ForeignKey(
        "catalog.UnidadMedida",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="items_matriz_precios_por_medida",
        verbose_name="unidad de la medida",
    )
    precio_base = models.DecimalField("precio base", max_digits=14, decimal_places=2)
    moneda = models.CharField(
        "moneda", max_length=3, choices=Moneda.choices, default=Moneda.USD
    )
    porcentaje_margen = models.DecimalField(
        "factor de margen",
        max_digits=5,
        decimal_places=4,
        help_text="Factor multiplicador (1.3000 = +30%)",
    )
    porcentaje_iva = models.DecimalField(
        "alícuota de IVA",
        max_digits=5,
        decimal_places=4,
        help_text="Alícuota (0.1600 = 16%)",
    )

    class Meta:
        verbose_name = "ítem de la matriz de precios"
        verbose_name_plural = "ítems de la matriz de precios"
        db_table = "precios.item_matriz_precios"
        ordering = ["-actualizado_en"]
        indexes = [
            models.Index(fields=["producto"], name="pricing_item_producto_idx"),
            models.Index(fields=["variante"], name="pricing_item_variante_idx"),
            models.Index(fields=["servicio"], name="pricing_item_servicio_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(
                        producto__isnull=False,
                        variante__isnull=True,
                        servicio__isnull=True,
                    )
                    | Q(
                        producto__isnull=True,
                        variante__isnull=False,
                        servicio__isnull=True,
                    )
                    | Q(
                        producto__isnull=True,
                        variante__isnull=True,
                        servicio__isnull=False,
                    )
                ),
                name="pricing_item_destino_excluyente",
            ),
            models.CheckConstraint(
                condition=(
                    Q(medida_cantidad__isnull=True, unidad_medida_medida__isnull=True)
                    | Q(
                        medida_cantidad__isnull=False,
                        unidad_medida_medida__isnull=False,
                    )
                ),
                name="pricing_item_medida_um_ck",
            ),
            models.CheckConstraint(
                condition=Q(precio_base__gte=0), name="pricing_item_precio_base_ck"
            ),
            models.CheckConstraint(
                condition=Q(porcentaje_margen__gt=0), name="pricing_item_margen_ck"
            ),
            models.CheckConstraint(
                condition=Q(porcentaje_iva__gte=0), name="pricing_item_iva_ck"
            ),
            models.CheckConstraint(
                condition=Q(moneda__in=Moneda.values), name="pricing_item_moneda_ck"
            ),
        ]

    def __str__(self):
        destino = self.variante or self.producto or self.servicio
        return f"{destino} - {self.precio_base} {self.moneda}"


class HistorialCambioPrecio(TimeStampedModel, ActivoMixin):
    """Registro inmutable (append-only) de cada cambio de precio base (RF-46).

    Hereda los mixins ``TimeStampedModel`` y ``ActivoMixin`` (estándar
    obligatorio del grupo); la protección append-only vive en ``save`` y
    ``delete``, que rechazan la modificación y el borrado de registros.
    """

    item_matriz = models.ForeignKey(
        ItemMatrizPrecios,
        on_delete=models.PROTECT,
        related_name="historial_cambios",
        verbose_name="ítem de la matriz",
    )
    precio_anterior = models.DecimalField(
        "precio anterior", max_digits=14, decimal_places=2
    )
    precio_nuevo = models.DecimalField("precio nuevo", max_digits=14, decimal_places=2)
    usuario = models.ForeignKey(
        "core.Usuario",
        on_delete=models.PROTECT,
        related_name="cambios_precio",
        verbose_name="modificado por",
    )
    cambiado_en = models.DateTimeField("cambiado en", auto_now_add=True)

    class Meta:
        verbose_name = "cambio de precio"
        verbose_name_plural = "historial de cambios de precio"
        db_table = "precios.historial_cambio_precio"
        ordering = ["-cambiado_en"]
        indexes = [
            models.Index(
                fields=["item_matriz", "-cambiado_en"],
                name="pricing_historial_item_idx",
            ),
        ]

    def __str__(self):
        return f"{self.item_matriz_id}: {self.precio_anterior} -> {self.precio_nuevo}"

    def save(self, *args, **kwargs):
        if self.pk:
            raise PermissionDenied(
                "Los registros de HistorialCambioPrecio son append-only "
                "y no pueden ser modificados."
            )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise PermissionDenied(
            "Los registros de HistorialCambioPrecio son append-only "
            "y no pueden ser eliminados."
        )


class ParametroFormula(TimeStampedModel, ActivoMixin):
    """Margen e IVA de la fórmula de precios, vigentes por rango de fechas (RF-45).

    El parámetro vigente es la fila con ``fecha_desde <= hoy < fecha_hasta``
    (o la última con ``fecha_hasta`` nulo).
    """

    porcentaje_margen = models.DecimalField(
        "factor de margen",
        max_digits=5,
        decimal_places=4,
        help_text="Factor multiplicador (1.3000 = +30%)",
    )
    porcentaje_iva = models.DecimalField(
        "alícuota de IVA",
        max_digits=5,
        decimal_places=4,
        help_text="Alícuota (0.1600 = 16%)",
    )
    fecha_desde = models.DateField("vigente desde")
    fecha_hasta = models.DateField(
        "vigente hasta",
        null=True,
        blank=True,
        help_text="Vacío = vigente hasta que exista el siguiente parámetro",
    )
    registrado_por = models.ForeignKey(
        "core.Usuario",
        on_delete=models.PROTECT,
        related_name="parametros_formula",
        verbose_name="registrado por",
    )

    class Meta:
        verbose_name = "parámetro de fórmula"
        verbose_name_plural = "parámetros de fórmula"
        db_table = "precios.parametro_formula"
        ordering = ["-fecha_desde"]
        constraints = [
            models.UniqueConstraint(
                fields=["fecha_desde"], name="pricing_parametro_formula_uk"
            ),
            models.CheckConstraint(
                condition=Q(porcentaje_margen__gt=0),
                name="pricing_parametro_margen_ck",
            ),
            models.CheckConstraint(
                condition=Q(porcentaje_iva__gte=0),
                name="pricing_parametro_iva_ck",
            ),
            models.CheckConstraint(
                condition=Q(fecha_hasta__isnull=True)
                | Q(fecha_hasta__gt=models.F("fecha_desde")),
                name="pricing_parametro_vigencia_ck",
            ),
        ]

    def __str__(self):
        hasta = self.fecha_hasta or "vigente"
        return (
            f"margen {self.porcentaje_margen} / IVA {self.porcentaje_iva} "
            f"({self.fecha_desde} - {hasta})"
        )
