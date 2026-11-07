from django.conf import settings
from django.db import models
from core.common.models import Auditable


class ItemMatrizPrecios(Auditable):
    producto = models.ForeignKey("catalog.Producto", on_delete=models.CASCADE, null=True, blank=True)
    servicio = models.ForeignKey("catalog.Servicio", on_delete=models.CASCADE, null=True, blank=True)
    material = models.ForeignKey("catalog.Material", on_delete=models.PROTECT, null=True, blank=True)
    medida = models.CharField(max_length=50, blank=True, default="")
    talla = models.ForeignKey("catalog.Talla", on_delete=models.PROTECT, null=True, blank=True)
    precio_base = models.DecimalField(max_digits=14, decimal_places=2)
    moneda = models.CharField(max_length=3, default="USD")
    porcentaje_margen = models.DecimalField(max_digits=5, decimal_places=4, default=1.3000)
    porcentaje_iva = models.DecimalField(max_digits=5, decimal_places=4, default=0.1600)
    estado = models.CharField(max_length=20, default="vigente")

    class Meta:
        db_table = "pricing_item_matriz_precios"
        verbose_name = "Ítem de Matriz de Precios"
        verbose_name_plural = "Ítems de Matriz de Precios"

    def __str__(self):
        desc = self.producto.nombre if self.producto else (self.servicio.nombre if self.servicio else "Ítem")
        return f"{desc} | Base: {self.precio_base} {self.moneda}"


class HistorialCambioPrecio(Auditable):
    item_matriz = models.ForeignKey(ItemMatrizPrecios, on_delete=models.CASCADE, related_name="historial_cambios")
    precio_anterior = models.DecimalField(max_digits=14, decimal_places=2)
    precio_nuevo = models.DecimalField(max_digits=14, decimal_places=2)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    cambiado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pricing_historial_cambio_precio"
        verbose_name = "Historial de Cambio de Precio"
        verbose_name_plural = "Historiales de Cambios de Precio"

    def __str__(self):
        return f"Cambio {self.precio_anterior} → {self.precio_nuevo}"
