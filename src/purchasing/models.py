from django.db import models
from core.common.models import Auditable


class Proveedor(Auditable):
    nombre = models.CharField(max_length=150)
    persona_contacto = models.CharField(max_length=100, blank=True, default="")
    telefono = models.CharField(max_length=30, blank=True, default="")
    rif = models.CharField(max_length=30, blank=True, default="")
    moneda_predeterminada = models.CharField(max_length=3, default="USD")

    class Meta:
        db_table = "purchasing_proveedor"
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre


class OrdenCompra(Auditable):
    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        CONFIRMADA = "confirmada", "Confirmada"
        RECIBIDA = "recibida", "Recibida"
        ANULADA = "anulada", "Anulada"

    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name="ordenes_compra")
    local = models.ForeignKey("identity.Local", on_delete=models.PROTECT, related_name="ordenes_compra")
    estado = models.CharField(max_length=30, choices=Estado.choices, default=Estado.BORRADOR)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    moneda = models.CharField(max_length=3, default="USD")

    class Meta:
        db_table = "purchasing_orden_compra"
        verbose_name = "Orden de Compra"
        verbose_name_plural = "Órdenes de Compra"

    def __str__(self):
        return f"OC #{self.id} - {self.proveedor.nombre} ({self.total} {self.moneda})"


class LineaOrdenCompra(Auditable):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name="lineas")
    material = models.ForeignKey("catalog.Material", on_delete=models.PROTECT)
    um = models.CharField(max_length=20)
    cantidad = models.DecimalField(max_digits=12, decimal_places=4)
    precio_unitario = models.DecimalField(max_digits=14, decimal_places=2)
    total_linea = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        db_table = "purchasing_linea_orden_compra"
        verbose_name = "Línea de Orden de Compra"
        verbose_name_plural = "Líneas de Orden de Compra"

    def __str__(self):
        return f"{self.material.nombre}: {self.cantidad} {self.um}"


class FacturaCompra(Auditable):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.SET_NULL, null=True, blank=True, related_name="facturas")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=14, decimal_places=2)
    moneda = models.CharField(max_length=3, default="USD")
    ruta_archivo = models.FileField(upload_to="facturas_compra/", blank=True, null=True)
    fecha_emision = models.DateField()

    class Meta:
        db_table = "purchasing_factura_compra"
        verbose_name = "Factura de Compra"
        verbose_name_plural = "Facturas de Compra"

    def __str__(self):
        return f"Factura {self.proveedor.nombre} - {self.total} {self.moneda} ({self.fecha_emision})"


class HistorialPrecioProveedor(Auditable):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="historial_precios")
    material = models.ForeignKey("catalog.Material", on_delete=models.CASCADE, related_name="historial_precios")
    um = models.CharField(max_length=20)
    precio_unitario = models.DecimalField(max_digits=14, decimal_places=2)
    moneda = models.CharField(max_length=3, default="USD")
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "purchasing_historial_precio_proveedor"
        indexes = [
            models.Index(fields=["proveedor", "material", "fecha_registro"]),
        ]
        verbose_name = "Historial de Precio de Proveedor"
        verbose_name_plural = "Historiales de Precios de Proveedores"

    def __str__(self):
        return f"{self.proveedor.nombre} | {self.material.nombre} = {self.precio_unitario} {self.moneda}"
