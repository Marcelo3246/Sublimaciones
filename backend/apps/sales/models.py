"""Modelos de datos para el módulo ventas.

Implementa clientes, pedidos de venta con sus líneas, cobros multi-moneda
y facturas propias con class Meta y db_table explícito.

Fuente: RF-36 a RF-43 (docs/03-requerimientos-del-sistema.md),
docs/modelo-datos/06.7-ventas.md y docs/ddl/06b.7-ventas.md.

Las notas de entrega son documentos generados por ``documents`` (RF-41),
no tablas de ventas.
"""

from django.db import models
from django.db.models import Q
from django.utils import timezone

from backend.apps.sales.choices import (
    EstadoFactura,
    EstadoPedido,
    MetodoCobro,
    Moneda,
    TipoFactura,
    TipoLineaPedido,
)
from backend.common.base_models import ActivoMixin, TimeStampedModel


class Cliente(TimeStampedModel, ActivoMixin):
    """Cliente del negocio; sin RIF se trata como consumidor final (RF-36)."""

    nombre = models.CharField("nombre o razón social", max_length=150)
    telefono = models.CharField("teléfono", max_length=30, blank=True, default="")
    correo = models.EmailField("correo", max_length=150, blank=True, default="")
    rif = models.CharField(
        "RIF / cédula",
        max_length=20,
        null=True,
        blank=True,
        help_text="Vacío = consumidor final",
    )

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        db_table = "ventas.cliente"
        ordering = ["nombre"]
        indexes = [
            models.Index(fields=["nombre"], name="sales_cliente_nombre_idx"),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.rif})" if self.rif else self.nombre


class PedidoVenta(TimeStampedModel, ActivoMixin):
    """Pedido de venta; su estado funciona como línea de producción (RF-37)."""

    codigo = models.CharField("código", max_length=30)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="pedidos",
        verbose_name="cliente",
    )
    local = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        related_name="pedidos_venta",
        verbose_name="local que vende",
    )
    estado = models.CharField(
        "estado",
        max_length=20,
        choices=EstadoPedido.choices,
        default=EstadoPedido.COTIZADO,
    )
    moneda = models.CharField(
        "moneda", max_length=3, choices=Moneda.choices, default=Moneda.USD
    )
    total = models.DecimalField("total", max_digits=14, decimal_places=2, default=0)
    # Referencia débil (sin FK en BD) al trabajador vendedor de rrhh.
    vendedor = models.ForeignKey(
        "hr.Trabajador",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_constraint=False,
        related_name="pedidos_vendidos",
        verbose_name="vendedor",
    )
    confirmado_en = models.DateTimeField("confirmado en", null=True, blank=True)
    fecha_compromiso = models.DateField("fecha de compromiso", null=True, blank=True)
    motivo_anulacion = models.CharField(
        "motivo de anulación", max_length=200, blank=True, default=""
    )

    class Meta:
        verbose_name = "pedido de venta"
        verbose_name_plural = "pedidos de venta"
        db_table = "ventas.pedido_venta"
        ordering = ["-creado_en"]
        indexes = [
            models.Index(
                fields=["estado", "local"], name="sales_pedido_estado_local_idx"
            ),
            models.Index(
                fields=["cliente", "-creado_en"], name="sales_pedido_cliente_idx"
            ),
        ]
        constraints = [
            models.UniqueConstraint(fields=["codigo"], name="sales_pedido_codigo_uk"),
            models.CheckConstraint(
                condition=Q(estado__in=EstadoPedido.values),
                name="sales_pedido_estado_ck",
            ),
            models.CheckConstraint(
                condition=Q(moneda__in=Moneda.values), name="sales_pedido_moneda_ck"
            ),
            models.CheckConstraint(
                condition=Q(total__gte=0), name="sales_pedido_total_ck"
            ),
            # Justificación obligatoria al anular (RF-43)
            models.CheckConstraint(
                condition=~Q(estado=EstadoPedido.ANULADO) | ~Q(motivo_anulacion=""),
                name="sales_pedido_anulacion_motivo_ck",
            ),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.cliente.nombre} ({self.get_estado_display()})"


class LineaPedido(TimeStampedModel, ActivoMixin):
    """Línea del pedido: producto, producto personalizado o servicio puro."""

    pedido_venta = models.ForeignKey(
        PedidoVenta,
        on_delete=models.CASCADE,
        related_name="lineas",
        verbose_name="pedido de venta",
    )
    tipo_linea = models.CharField(
        "tipo de línea",
        max_length=30,
        choices=TipoLineaPedido.choices,
        default=TipoLineaPedido.PRODUCTO,
    )
    variante = models.ForeignKey(
        "catalog.VarianteProducto",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="lineas_pedido",
        verbose_name="variante",
    )
    servicio = models.ForeignKey(
        "catalog.Servicio",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="lineas_pedido",
        verbose_name="servicio",
    )
    material = models.ForeignKey(
        "catalog.Material",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="lineas_pedido",
        verbose_name="material",
    )
    unidad_medida = models.ForeignKey(
        "catalog.UnidadMedida",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="lineas_pedido",
        verbose_name="unidad de medida",
    )
    medida_cantidad = models.DecimalField(
        "medida", max_digits=12, decimal_places=4, null=True, blank=True
    )
    unidad_medida_medida = models.ForeignKey(
        "catalog.UnidadMedida",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="lineas_pedido_por_medida",
        verbose_name="unidad de la medida",
    )
    cantidad = models.DecimalField("cantidad", max_digits=12, decimal_places=4)
    precio_unitario = models.DecimalField(
        "precio unitario",
        max_digits=14,
        decimal_places=2,
        help_text="Snapshot del precio al cotizar (RF-39)",
    )
    moneda = models.CharField(
        "moneda", max_length=3, choices=Moneda.choices, default=Moneda.USD
    )
    # Referencia débil (sin FK en BD) al ítem de la matriz que cotizó.
    item_precio = models.ForeignKey(
        "pricing.ItemMatrizPrecios",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_constraint=False,
        related_name="lineas_pedido",
        verbose_name="ítem de la matriz de precios",
    )
    nota = models.CharField("nota", max_length=300, blank=True, default="")

    class Meta:
        verbose_name = "línea de pedido"
        verbose_name_plural = "líneas de pedido"
        db_table = "ventas.linea_pedido"
        ordering = ["pedido_venta", "id"]
        indexes = [
            models.Index(fields=["pedido_venta"], name="sales_linea_pedido_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(tipo_linea__in=TipoLineaPedido.values),
                name="sales_linea_tipo_ck",
            ),
            models.CheckConstraint(
                condition=~Q(
                    tipo_linea__in=[
                        TipoLineaPedido.PRODUCTO,
                        TipoLineaPedido.PRODUCTO_PERSONALIZADO,
                    ]
                )
                | Q(variante__isnull=False),
                name="sales_linea_producto_variante_ck",
            ),
            models.CheckConstraint(
                condition=~Q(tipo_linea=TipoLineaPedido.SERVICIO_PURO)
                | Q(servicio__isnull=False),
                name="sales_linea_servicio_ck",
            ),
            models.CheckConstraint(
                condition=~Q(tipo_linea=TipoLineaPedido.PRODUCTO_PERSONALIZADO)
                | Q(material__isnull=False),
                name="sales_linea_personalizado_material_ck",
            ),
            models.CheckConstraint(
                condition=(
                    Q(medida_cantidad__isnull=True, unidad_medida_medida__isnull=True)
                    | Q(
                        medida_cantidad__isnull=False,
                        unidad_medida_medida__isnull=False,
                    )
                ),
                name="sales_linea_medida_um_ck",
            ),
            models.CheckConstraint(
                condition=Q(cantidad__gt=0), name="sales_linea_cantidad_ck"
            ),
            models.CheckConstraint(
                condition=Q(precio_unitario__gte=0), name="sales_linea_precio_ck"
            ),
            models.CheckConstraint(
                condition=Q(moneda__in=Moneda.values), name="sales_linea_moneda_ck"
            ),
        ]

    def __str__(self):
        destino = self.variante or self.servicio
        return f"{self.pedido_venta.codigo}: {self.cantidad} x {destino}"


class Cobro(TimeStampedModel, ActivoMixin):
    """Cobro (parcial o total) de un pedido en USD o Bs. (RF-42).

    ``activo=False`` + ``anulado_en`` marcan un cobro anulado.
    """

    pedido_venta = models.ForeignKey(
        PedidoVenta,
        on_delete=models.PROTECT,
        related_name="cobros",
        verbose_name="pedido de venta",
    )
    monto = models.DecimalField("monto", max_digits=14, decimal_places=2)
    moneda = models.CharField(
        "moneda", max_length=3, choices=Moneda.choices, default=Moneda.USD
    )
    metodo = models.CharField(
        "método de pago", max_length=20, choices=MetodoCobro.choices
    )
    referencia = models.CharField(
        "referencia bancaria", max_length=100, blank=True, default=""
    )
    tasa_aplicada = models.ForeignKey(
        "core.TasaCambio",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="cobros",
        verbose_name="tasa de cambio aplicada",
        help_text="Obligatoria si se cobra en Bs.",
    )
    fecha = models.DateTimeField("fecha", default=timezone.now)
    anulado_en = models.DateTimeField("anulado en", null=True, blank=True)

    class Meta:
        verbose_name = "cobro"
        verbose_name_plural = "cobros"
        db_table = "ventas.cobro"
        ordering = ["-fecha"]
        indexes = [
            models.Index(fields=["pedido_venta"], name="sales_cobro_pedido_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(monto__gt=0), name="sales_cobro_monto_ck"
            ),
            models.CheckConstraint(
                condition=Q(moneda__in=Moneda.values), name="sales_cobro_moneda_ck"
            ),
            models.CheckConstraint(
                condition=Q(metodo__in=MetodoCobro.values),
                name="sales_cobro_metodo_ck",
            ),
            models.CheckConstraint(
                condition=~Q(moneda=Moneda.VES) | Q(tasa_aplicada__isnull=False),
                name="sales_cobro_tasa_bs_ck",
            ),
        ]

    def __str__(self):
        return f"{self.pedido_venta.codigo}: {self.monto} {self.moneda} ({self.metodo})"


class Factura(TimeStampedModel, ActivoMixin):
    """Factura propia con correlativo por (tipo, local, año) (RF-40, RF-43)."""

    pedido_venta = models.ForeignKey(
        PedidoVenta,
        on_delete=models.PROTECT,
        related_name="facturas",
        verbose_name="pedido de venta",
    )
    local = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        related_name="facturas",
        verbose_name="local",
    )
    numero = models.CharField("número", max_length=20)
    anio = models.PositiveSmallIntegerField("año")
    tipo = models.CharField(
        "tipo", max_length=10, choices=TipoFactura.choices, default=TipoFactura.PROPIA
    )
    estado = models.CharField(
        "estado",
        max_length=10,
        choices=EstadoFactura.choices,
        default=EstadoFactura.EMITIDA,
    )
    total = models.DecimalField("total", max_digits=14, decimal_places=2)
    moneda = models.CharField(
        "moneda", max_length=3, choices=Moneda.choices, default=Moneda.USD
    )
    fecha_emision = models.DateField("fecha de emisión", default=timezone.localdate)
    motivo_anulacion = models.CharField(
        "motivo de anulación", max_length=200, blank=True, default=""
    )
    emitida_por = models.ForeignKey(
        "core.Usuario",
        on_delete=models.PROTECT,
        related_name="facturas_emitidas",
        verbose_name="emitida por",
    )

    class Meta:
        verbose_name = "factura"
        verbose_name_plural = "facturas"
        db_table = "ventas.factura"
        ordering = ["-fecha_emision", "-numero"]
        indexes = [
            models.Index(
                fields=["tipo", "local", "fecha_emision"],
                name="sales_factura_repo_idx",
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["tipo", "local", "anio", "numero"],
                name="sales_factura_correlativo_uk",
            ),
            models.CheckConstraint(
                condition=Q(tipo__in=TipoFactura.values), name="sales_factura_tipo_ck"
            ),
            models.CheckConstraint(
                condition=Q(estado__in=EstadoFactura.values),
                name="sales_factura_estado_ck",
            ),
            models.CheckConstraint(
                condition=Q(total__gte=0), name="sales_factura_total_ck"
            ),
            models.CheckConstraint(
                condition=Q(moneda__in=Moneda.values), name="sales_factura_moneda_ck"
            ),
            models.CheckConstraint(
                condition=~Q(estado=EstadoFactura.ANULADA) | ~Q(motivo_anulacion=""),
                name="sales_factura_anulacion_ck",
            ),
        ]

    def __str__(self):
        return f"{self.get_tipo_display()} {self.numero}/{self.anio} - {self.local}"
