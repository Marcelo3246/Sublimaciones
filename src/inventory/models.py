from django.db import models
from core.common.models import Auditable


class Existencia(Auditable):
    class Tipo(models.TextChoices):
        MATERIAL = "material", "Material"
        PRODUCTO = "producto", "Producto"

    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    material = models.ForeignKey("catalog.Material", on_delete=models.CASCADE, null=True, blank=True, related_name="existencias")
    producto = models.ForeignKey("catalog.Producto", on_delete=models.CASCADE, null=True, blank=True, related_name="existencias")
    local = models.ForeignKey("identity.Local", on_delete=models.PROTECT, related_name="existencias")
    um = models.CharField(max_length=20)
    cantidad_disponible = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    estado = models.CharField(max_length=30, default="disponible")

    class Meta:
        db_table = "inventory_existencia"
        indexes = [
            models.Index(fields=["local", "activo"]),
        ]
        verbose_name = "Existencia"
        verbose_name_plural = "Existencias"

    def __str__(self):
        item = self.material.nombre if self.tipo == "material" and self.material else (self.producto.nombre if self.producto else "Item")
        return f"{item} - Local: {self.local.codigo} ({self.cantidad_disponible} {self.um})"


class Partida(Auditable):
    class Estado(models.TextChoices):
        DISPONIBLE = "disponible", "Disponible"
        RESERVADA = "reservada", "Reservada"
        EN_TRANSITO = "en_transito", "En Tránsito"
        DANADA = "danada", "Dañada"
        DESPERDICIO = "desperdicio", "Desperdicio"
        AGOTADA = "agotada", "Agotada"

    material = models.ForeignKey("catalog.Material", on_delete=models.PROTECT, related_name="partidas")
    local = models.ForeignKey("identity.Local", on_delete=models.PROTECT, related_name="partidas")
    codigo_partida = models.CharField(max_length=50, unique=True, help_text="Código o lote del rollo/partida")
    cantidad_inicial = models.DecimalField(max_digits=12, decimal_places=4)
    cantidad_restante = models.DecimalField(max_digits=12, decimal_places=4)
    um = models.CharField(max_length=20)
    estado = models.CharField(max_length=30, choices=Estado.choices, default=Estado.DISPONIBLE)
    motivo_descarte = models.TextField(blank=True, default="")

    class Meta:
        db_table = "inventory_partida"
        indexes = [
            models.Index(fields=["codigo_partida"]),
        ]
        verbose_name = "Partida / Rollo"
        verbose_name_plural = "Partidas / Rollos"

    def __str__(self):
        return f"{self.codigo_partida} ({self.material.nombre}) - {self.cantidad_restante}/{self.cantidad_inicial} {self.um}"


class MovimientoStock(Auditable):
    class TipoMovimiento(models.TextChoices):
        ENTRADA_COMPRA = "entrada_compra", "Entrada por compra"
        ENTRADA_PRODUCCION = "entrada_produccion", "Entrada por producción terminada"
        SALIDA_TRANSFERENCIA = "salida_transferencia", "Salida por transferencia"
        ENTRADA_TRANSFERENCIA = "entrada_transferencia", "Entrada por transferencia"
        SALIDA_VENTA = "salida_venta", "Salida por venta"
        DESPERDICIO = "desperdicio", "Baja por desperdicio"
        AJUSTE = "ajuste", "Ajuste manual de inventario"
        RESERVA = "reserva", "Reserva para orden de producción"

    tipo_movimiento = models.CharField(max_length=50, choices=TipoMovimiento.choices)
    local = models.ForeignKey("identity.Local", on_delete=models.PROTECT, related_name="movimientos_stock_origen")
    partida = models.ForeignKey(Partida, on_delete=models.SET_NULL, null=True, blank=True, related_name="movimientos")
    item_id = models.IntegerField(null=True, blank=True)
    tipo_item = models.CharField(max_length=20, blank=True, default="")
    local_destino = models.ForeignKey("identity.Local", on_delete=models.SET_NULL, null=True, blank=True, related_name="movimientos_stock_destino")
    um = models.CharField(max_length=20)
    cantidad = models.DecimalField(max_digits=12, decimal_places=4)
    motivo = models.TextField(blank=True, default="")

    class Meta:
        db_table = "inventory_movimiento_stock"
        verbose_name = "Movimiento de Stock"
        verbose_name_plural = "Movimientos de Stock"

    def __str__(self):
        return f"{self.get_tipo_movimiento_display()} ({self.cantidad} {self.um}) en Local {self.local.codigo}"


class GuiaTransferencia(Auditable):
    class Estado(models.TextChoices):
        SOLICITADA = "solicitada", "Solicitada"
        DESPACHADA = "despachada", "Despachada"
        EN_TRANSITO = "en_transito", "En Tránsito"
        RECIBIDA = "recibida", "Recibida"
        ANULADA = "anulada", "Anulada"

    codigo_guia = models.CharField(max_length=50, unique=True)
    local_origen = models.ForeignKey("identity.Local", on_delete=models.PROTECT, related_name="guias_transferencia_origen")
    local_destino = models.ForeignKey("identity.Local", on_delete=models.PROTECT, related_name="guias_transferencia_destino")
    estado = models.CharField(max_length=30, choices=Estado.choices, default=Estado.SOLICITADA)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_despacho = models.DateTimeField(null=True, blank=True)
    fecha_recepcion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "inventory_guia_transferencia"
        verbose_name = "Guía de Transferencia"
        verbose_name_plural = "Guías de Transferencia"

    def __str__(self):
        return f"{self.codigo_guia}: {self.local_origen.codigo} → {self.local_destino.codigo} ({self.get_estado_display()})"
