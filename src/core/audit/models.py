from django.conf import settings
from django.db import models


class BitacoraAccion(models.Model):
    """Bitácora append-only de acciones realizadas por los usuarios en el sistema.

    Registra quién, qué entidad, qué acción, valores antes/después, fecha-hora e IP.
    RNF-04: Tabla append-only; no permite UPDATE ni DELETE.
    """

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="acciones_auditadas",
    )
    modulo = models.CharField(max_length=50, help_text="Módulo del sistema, ej: 'sales', 'inventory'")
    entidad = models.CharField(max_length=100, help_text="Nombre del modelo afectado")
    entidad_id = models.IntegerField(null=True, blank=True)
    accion = models.CharField(max_length=50, default="modificar", help_text="crear, modificar, eliminar, login, etc.")
    estado_anterior = models.JSONField(null=True, blank=True, help_text="Snapshot previo en JSON")
    estado_nuevo = models.JSONField(null=True, blank=True, help_text="Snapshot posterior en JSON")
    direccion_ip = models.GenericIPAddressField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_bitacora_accion"
        ordering = ["-creado_en"]
        verbose_name = "Bitácora de Acción"
        verbose_name_plural = "Bitácoras de Acciones"

    def __str__(self):
        return f"[{self.creado_en}] {self.usuario} - {self.modulo}.{self.entidad} ({self.accion})"


class BitacoraStock(models.Model):
    """Bitácora append-only de todos los movimientos y ajustes que afectan el stock.

    RNF-04: Cada entrada, salida, ajuste, transferencia o cambio de estado queda registrado aquí.
    """

    local = models.ForeignKey(
        "identity.Local",
        on_delete=models.PROTECT,
        related_name="movimientos_stock_auditados",
    )
    tipo_item = models.CharField(max_length=20, help_text="'material' o 'producto'")
    item_id = models.IntegerField(help_text="ID del material o producto en su catálogo")
    tipo_movimiento = models.CharField(
        max_length=50,
        help_text="entrada_compra, salida_venta, consumo_produccion, transferencia, desperdicio, etc.",
    )
    partida_id = models.IntegerField(null=True, blank=True, help_text="ID de la partida si aplica")
    usuario_id = models.IntegerField(null=True, blank=True, help_text="ID del usuario que ejecutó la acción")
    cantidad = models.DecimalField(max_digits=12, decimal_places=4)
    um = models.CharField(max_length=20, help_text="Unidad de medida")
    motivo = models.TextField(blank=True, default="")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_bitacora_stock"
        ordering = ["-creado_en"]
        verbose_name = "Bitácora de Stock"
        verbose_name_plural = "Bitácoras de Stock"

    def __str__(self):
        return f"[{self.creado_en}] Local {self.local_id}: {self.tipo_movimiento} ({self.cantidad} {self.um})"
