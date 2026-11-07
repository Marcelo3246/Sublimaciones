from django.conf import settings
from django.db import models
from core.common.models import Auditable


class Cliente(Auditable):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30, blank=True, default="")
    correo = models.EmailField(blank=True, default="")
    rif = models.CharField(max_length=30, blank=True, default="")

    class Meta:
        db_table = "sales_cliente"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nombre


class PedidoVenta(Auditable):
    class Estado(models.TextChoices):
        COTIZADO = "cotizado", "Cotizado"
        CONFIRMADO = "confirmado", "Confirmado"
        EN_PRODUCCION = "en_produccion", "En Producción"
        LISTO = "listo", "Listo para Entrega"
        ENTREGADO = "entregado", "Entregado"
        FACTURADO = "facturado", "Facturado"
        ANULADO = "anulado", "Anulado"

    codigo_pedido = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, null=True, blank=True, related_name="pedidos")
    local = models.ForeignKey("identity.Local", on_delete=models.PROTECT, related_name="pedidos_venta")
    estado = models.CharField(max_length=30, choices=Estado.choices, default=Estado.COTIZADO)
    moneda = models.CharField(max_length=3, default="USD")
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    tipo_cobro = models.CharField(
        max_length=30,
        choices=[
            ("efectivo", "Efectivo"),
            ("punto", "Punto de Venta"),
            ("transferencia", "Transferencia"),
            ("divisa", "Divisa"),
        ],
        blank=True,
        default="",
    )
    vendedor_trabajador_id = models.IntegerField(null=True, blank=True)
    confirmado_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "sales_pedido_venta"
        indexes = [
            models.Index(fields=["estado", "local"]),
        ]
        verbose_name = "Pedido de Venta"
        verbose_name_plural = "Pedidos de Venta"

    def __str__(self):
        return f"{self.codigo_pedido} - {self.get_estado_display()} ({self.total} {self.moneda})"


class LineaPedido(Auditable):
    class TipoLinea(models.TextChoices):
        PRODUCTO = "producto", "Producto Estándar"
        SERVICIO_PURO = "servicio_puro", "Servicio Puro"
        PRODUCTO_PERSONALIZADO = "producto_personalizado", "Producto Personalizado"

    pedido = models.ForeignKey(PedidoVenta, on_delete=models.CASCADE, related_name="lineas")
    tipo_linea = models.CharField(max_length=30, choices=TipoLinea.choices, default=TipoLinea.PRODUCTO)
    producto = models.ForeignKey("catalog.Producto", on_delete=models.PROTECT, null=True, blank=True)
    servicio = models.ForeignKey("catalog.Servicio", on_delete=models.PROTECT, null=True, blank=True)
    material = models.ForeignKey("catalog.Material", on_delete=models.PROTECT, null=True, blank=True)
    um = models.CharField(max_length=20, blank=True, default="")
    medida = models.CharField(max_length=50, blank=True, default="")
    talla = models.ForeignKey("catalog.Talla", on_delete=models.PROTECT, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=12, decimal_places=4)
    precio_unitario = models.DecimalField(max_digits=14, decimal_places=2)
    moneda = models.CharField(max_length=3, default="USD")

    class Meta:
        db_table = "sales_linea_pedido"
        verbose_name = "Línea de Pedido"
        verbose_name_plural = "Líneas de Pedido"

    def __str__(self):
        return f"Línea #{self.id} de {self.pedido.codigo_pedido}"


class Factura(Auditable):
    class Tipo(models.TextChoices):
        PROPIA = "propia", "Propia"
        FISCAL = "fiscal", "Fiscal (SENIAT diferido)"

    class Estado(models.TextChoices):
        EMITIDA = "emitida", "Emitida"
        ANULADA = "anulada", "Anulada"

    pedido = models.ForeignKey(PedidoVenta, on_delete=models.PROTECT, related_name="facturas")
    local = models.ForeignKey("identity.Local", on_delete=models.PROTECT, related_name="facturas_emitidas")
    numero_factura = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.PROPIA)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.EMITIDA)
    fecha_emision = models.DateField()
    emitida_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        db_table = "sales_factura"
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"

    def __str__(self):
        return f"Factura #{self.numero_factura} ({self.local.codigo})"
