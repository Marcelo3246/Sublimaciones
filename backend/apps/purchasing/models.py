"""Modelos de datos del módulo compras (abastecimiento).

Implementa empresas, proveedores, órdenes de compra y recepción,
facturas de compra e historial de precios con class Meta y db_table
explícito (ver tasks/tareas-grupo-base-de-datos.md).

Semántica: docs/modelo-datos/06.5-compras.md y docs/ddl/06b.5-compras.md
(RF-25 a RF-29).
"""

from django.db import models
from django.utils import timezone

from backend.apps.purchasing.choices import (
    EstadoOrdenCompra,
    EstadoRecepcionCompra,
    Moneda,
)
from backend.common.base_models import ActivoMixin, TimeStampedModel


class Empresa(TimeStampedModel, ActivoMixin):
    """Compañía que vende insumos; varios proveedores pueden pertenecer a ella."""

    nombre = models.CharField("nombre", max_length=150)
    rif = models.CharField("RIF", max_length=20, unique=True)
    direccion = models.CharField("dirección", max_length=200, blank=True, default="")
    telefono = models.CharField("teléfono", max_length=30, blank=True, default="")
    correo = models.CharField("correo", max_length=150, blank=True, default="")

    class Meta:
        verbose_name = "empresa"
        verbose_name_plural = "empresas"
        db_table = "compras.empresa"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.rif} - {self.nombre}"


class Proveedor(TimeStampedModel, ActivoMixin):
    """Punto de contacto concreto de una empresa proveedora (RF-25)."""

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.PROTECT,
        related_name="proveedores",
        verbose_name="empresa",
    )
    persona_contacto = models.CharField("persona de contacto", max_length=100)
    telefono = models.CharField("teléfono", max_length=30, blank=True, default="")
    correo = models.CharField("correo", max_length=150, blank=True, default="")
    moneda_predeterminada = models.CharField(
        "moneda predeterminada",
        max_length=3,
        choices=Moneda.choices,
        default=Moneda.USD,
    )
    condiciones_pago = models.CharField(
        "condiciones de pago", max_length=200, blank=True, default=""
    )
    calificacion = models.PositiveSmallIntegerField(
        "calificación",
        null=True,
        blank=True,
        help_text="Puntaje del proveedor de 1 a 5",
    )

    class Meta:
        verbose_name = "proveedor"
        verbose_name_plural = "proveedores"
        db_table = "compras.proveedor"
        ordering = ["persona_contacto"]
        indexes = [
            models.Index(
                fields=["empresa", "activo"],
                name="purchasing_prov_empresa_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(calificacion__isnull=True)
                | models.Q(calificacion__gte=1, calificacion__lte=5),
                name="purchasing_proveedor_calif_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(moneda_predeterminada__in=Moneda.values),
                name="purchasing_proveedor_moneda_ck",
            ),
        ]

    def __str__(self):
        return f"{self.persona_contacto} ({self.empresa.nombre})"


class OrdenCompra(TimeStampedModel, ActivoMixin):
    """Orden de compra dirigida a un proveedor para un local (RF-26)."""

    numero_orden = models.CharField(
        "número de orden",
        max_length=30,
        unique=True,
        null=True,
        blank=True,
        help_text="Correlativo propio; vacío hasta activar ContadorCorrelativo",
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name="ordenes_compra",
        verbose_name="proveedor",
    )
    local = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        related_name="ordenes_compra",
        verbose_name="local destino",
    )
    estado = models.CharField(
        "estado",
        max_length=20,
        choices=EstadoOrdenCompra.choices,
        default=EstadoOrdenCompra.BORRADOR,
    )
    total = models.DecimalField(
        "total", max_digits=14, decimal_places=2, default=0
    )
    moneda = models.CharField(
        "moneda", max_length=3, choices=Moneda.choices, default=Moneda.USD
    )
    fecha_emision = models.DateField("fecha de emisión", default=timezone.now)
    fecha_envio = models.DateField("fecha de envío", null=True, blank=True)

    class Meta:
        verbose_name = "orden de compra"
        verbose_name_plural = "órdenes de compra"
        db_table = "compras.orden_compra"
        ordering = ["-fecha_emision", "-creado_en"]
        indexes = [
            models.Index(
                fields=["local", "estado"],
                name="purchasing_oc_local_estado_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(total__gte=0),
                name="purchasing_oc_total_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(estado__in=EstadoOrdenCompra.values),
                name="purchasing_oc_estado_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(moneda__in=Moneda.values),
                name="purchasing_oc_moneda_ck",
            ),
        ]

    def __str__(self):
        return f"OC-{self.numero_orden or self.pk} ({self.get_estado_display()})"


class LineaOrdenCompra(TimeStampedModel, ActivoMixin):
    """Ítem de material solicitado en una orden de compra."""

    orden_compra = models.ForeignKey(
        OrdenCompra,
        on_delete=models.CASCADE,
        related_name="lineas",
        verbose_name="orden de compra",
    )
    material = models.ForeignKey(
        "catalog.Material",
        on_delete=models.PROTECT,
        related_name="lineas_orden_compra",
        verbose_name="material",
    )
    unidad_medida = models.ForeignKey(
        "catalog.UnidadMedida",
        on_delete=models.PROTECT,
        related_name="lineas_orden_compra",
        verbose_name="unidad de medida",
    )
    cantidad_solicitada = models.DecimalField(
        "cantidad solicitada", max_digits=12, decimal_places=4
    )
    cantidad_recibida = models.DecimalField(
        "cantidad recibida",
        max_digits=12,
        decimal_places=4,
        default=0,
    )
    precio_unitario = models.DecimalField(
        "precio unitario", max_digits=14, decimal_places=2
    )
    moneda = models.CharField(
        "moneda", max_length=3, choices=Moneda.choices, default=Moneda.USD
    )

    class Meta:
        verbose_name = "línea de orden de compra"
        verbose_name_plural = "líneas de orden de compra"
        db_table = "compras.linea_orden_compra"
        ordering = ["id"]
        indexes = [
            models.Index(
                fields=["orden_compra"],
                name="purchasing_linea_orden_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad_solicitada__gt=0),
                name="purchasing_linea_solicitada_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(cantidad_recibida__gte=0),
                name="purchasing_linea_recibida_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(cantidad_recibida__lte=models.F("cantidad_solicitada")),
                name="purchasing_linea_max_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(precio_unitario__gte=0),
                name="purchasing_linea_precio_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(moneda__in=Moneda.values),
                name="purchasing_linea_moneda_ck",
            ),
        ]

    def __str__(self):
        return f"{self.material} x {self.cantidad_solicitada}"


class RecepcionCompra(TimeStampedModel, ActivoMixin):
    """Recepción de mercancía contra una orden; dispara la entrada al stock."""

    orden_compra = models.ForeignKey(
        OrdenCompra,
        on_delete=models.PROTECT,
        related_name="recepciones",
        verbose_name="orden de compra",
    )
    local = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        related_name="recepciones_compra",
        verbose_name="local que recibe",
    )
    estado = models.CharField(
        "estado",
        max_length=20,
        choices=EstadoRecepcionCompra.choices,
        default=EstadoRecepcionCompra.PENDIENTE,
    )
    fecha_recepcion = models.DateField("fecha de recepción", default=timezone.now)
    numero_guia_proveedor = models.CharField(
        "número de guía del proveedor",
        max_length=50,
        blank=True,
        default="",
    )
    observacion = models.CharField(
        "observación", max_length=300, blank=True, default=""
    )

    class Meta:
        verbose_name = "recepción de compra"
        verbose_name_plural = "recepciones de compra"
        db_table = "compras.recepcion_compra"
        ordering = ["-fecha_recepcion", "-creado_en"]
        indexes = [
            models.Index(
                fields=["orden_compra", "estado"],
                name="purchasing_recep_ord_est_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(estado__in=EstadoRecepcionCompra.values),
                name="purchasing_recep_estado_ck",
            ),
        ]

    def __str__(self):
        return f"Recepción {self.pk} de {self.orden_compra} ({self.get_estado_display()})"


class LineaRecepcionCompra(TimeStampedModel, ActivoMixin):
    """Cantidad recibida por línea de la orden; acumula recepciones parciales."""

    recepcion_compra = models.ForeignKey(
        RecepcionCompra,
        on_delete=models.CASCADE,
        related_name="lineas",
        verbose_name="recepción",
    )
    linea_orden_compra = models.ForeignKey(
        LineaOrdenCompra,
        on_delete=models.PROTECT,
        related_name="recepciones",
        verbose_name="línea de orden",
    )
    cantidad_recibida = models.DecimalField(
        "cantidad recibida", max_digits=12, decimal_places=4
    )
    unidad_medida = models.ForeignKey(
        "catalog.UnidadMedida",
        on_delete=models.PROTECT,
        related_name="lineas_recepcion_compra",
        verbose_name="unidad de medida",
    )
    lote = models.ForeignKey(
        "inventory.Lote",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="recepciones_compra",
        verbose_name="lote",
        help_text="Lote generado solo si el material es continuo",
    )

    class Meta:
        verbose_name = "línea de recepción"
        verbose_name_plural = "líneas de recepción"
        db_table = "compras.linea_recepcion_compra"
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad_recibida__gt=0),
                name="purchasing_linea_recep_cantidad_ck",
            ),
        ]

    def __str__(self):
        return f"Recibido {self.cantidad_recibida} en recepción {self.recepcion_compra_id}"


class FacturaCompra(TimeStampedModel, ActivoMixin):
    """Factura de un proveedor, con o sin vínculo a orden/recepción (RF-27)."""

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name="facturas_compra",
        verbose_name="proveedor",
    )
    orden_compra = models.ForeignKey(
        OrdenCompra,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="facturas_compra",
        verbose_name="orden de compra",
    )
    recepcion_compra = models.ForeignKey(
        RecepcionCompra,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="facturas_compra",
        verbose_name="recepción",
    )
    numero_externo = models.CharField(
        "número externo",
        max_length=50,
        blank=True,
        default="",
        help_text="Número impreso por el proveedor",
    )
    fecha_emision = models.DateField("fecha de emisión", default=timezone.now)
    total = models.DecimalField("total", max_digits=14, decimal_places=2)
    moneda = models.CharField(
        "moneda", max_length=3, choices=Moneda.choices, default=Moneda.USD
    )
    tasa_aplicada = models.ForeignKey(
        "core.TasaCambio",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="facturas_compra",
        verbose_name="tasa aplicada",
        help_text="Tasa del día usada como evidencia de conversión (RF-29)",
    )
    ruta_archivo = models.CharField(
        "ruta del archivo",
        max_length=500,
        blank=True,
        default="",
        help_text="PDF o imagen adjunta de la factura",
    )

    class Meta:
        verbose_name = "factura de compra"
        verbose_name_plural = "facturas de compra"
        db_table = "compras.factura_compra"
        ordering = ["-fecha_emision", "-creado_en"]
        indexes = [
            models.Index(
                fields=["proveedor", "fecha_emision"],
                name="purchasing_fact_prov_fecha_idx",
            ),
            models.Index(
                fields=["moneda", "fecha_emision"],
                name="purchasing_fact_mon_fecha_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(total__gte=0),
                name="purchasing_fact_total_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(moneda__in=Moneda.values),
                name="purchasing_fact_moneda_ck",
            ),
        ]

    def __str__(self):
        return f"Factura {self.numero_externo or self.pk} - {self.proveedor}"


class HistorialPrecioProveedor(TimeStampedModel, ActivoMixin):
    """Precio de un material por proveedor en el tiempo (comparador RF-28)."""

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name="historial_precios",
        verbose_name="proveedor",
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.PROTECT,
        related_name="historial_precios",
        verbose_name="empresa",
        help_text="Heredado de la empresa para agrupar por vendedor",
    )
    material = models.ForeignKey(
        "catalog.Material",
        on_delete=models.PROTECT,
        related_name="historial_precios_proveedor",
        verbose_name="material",
    )
    unidad_medida = models.ForeignKey(
        "catalog.UnidadMedida",
        on_delete=models.PROTECT,
        related_name="historial_precios_proveedor",
        verbose_name="unidad de medida",
    )
    precio_unitario = models.DecimalField(
        "precio unitario", max_digits=14, decimal_places=2
    )
    moneda = models.CharField(
        "moneda", max_length=3, choices=Moneda.choices, default=Moneda.USD
    )
    registrado_en = models.DateTimeField("registrado en", auto_now_add=True)

    class Meta:
        verbose_name = "historial de precio de proveedor"
        verbose_name_plural = "historiales de precios de proveedores"
        db_table = "compras.historial_precio_proveedor"
        ordering = ["-registrado_en"]
        indexes = [
            models.Index(
                fields=["material", "proveedor", "-registrado_en"],
                name="purchasing_hist_precio_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(precio_unitario__gte=0),
                name="purchasing_hist_precio_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(moneda__in=Moneda.values),
                name="purchasing_hist_moneda_ck",
            ),
        ]

    def __str__(self):
        return f"{self.material} - {self.proveedor}: {self.precio_unitario}"
