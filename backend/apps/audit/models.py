"""Modelos de datos para el módulo auditoría.

Implementa bitácoras append-only para trazabilidad transversal de acciones
de usuario y movimientos físicos de stock.
"""

from django.core.exceptions import PermissionDenied
from django.db import models

from backend.apps.audit.choices import AccionAuditoria, TipoMovimientoStock


class BitacoraAccion(models.Model):
    """Bitácora inmutable (append-only) de acciones y eventos de usuarios."""

    usuario = models.ForeignKey(
        "core.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="acciones_auditadas",
        verbose_name="usuario",
    )
    local = models.ForeignKey(
        "core.Local",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="acciones_auditadas",
        verbose_name="local",
    )
    modulo = models.CharField("módulo", max_length=50, blank=True, default="")
    accion = models.CharField(
        "acción", max_length=30, choices=AccionAuditoria.choices
    )
    entidad = models.CharField("entidad", max_length=100)
    entidad_id = models.BigIntegerField("ID de entidad", null=True, blank=True)
    datos_antes = models.JSONField("datos anteriores", null=True, blank=True)
    datos_despues = models.JSONField("datos posteriores", null=True, blank=True)
    ip_origen = models.GenericIPAddressField("IP de origen", null=True, blank=True)
    creado_en = models.DateTimeField("fecha y hora", auto_now_add=True)

    class Meta:
        verbose_name = "bitácora de acción"
        verbose_name_plural = "bitácoras de acciones"
        db_table = "auditoria.bitacora_accion"
        ordering = ["-creado_en"]
        indexes = [
            models.Index(
                fields=["usuario", "-creado_en"],
                name="audit_accion_usr_idx",
            ),
            models.Index(
                fields=["modulo", "entidad", "entidad_id"],
                name="audit_accion_ent_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(accion__in=AccionAuditoria.values),
                name="audit_accion_tipo_ck",
            ),
        ]

    def __str__(self):
        usuario_str = self.usuario.nombre_usuario if self.usuario else "Sistema"
        return f"[{self.creado_en:%Y-%m-%d %H:%M}] {usuario_str} - {self.accion} {self.entidad}"

    def save(self, *args, **kwargs):
        if self.pk:
            raise PermissionDenied(
                "Los registros de BitacoraAccion son append-only y no pueden ser modificados."
            )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise PermissionDenied(
            "Los registros de BitacoraAccion son append-only y no pueden ser eliminados."
        )


class BitacoraStock(models.Model):
    """Bitácora inmutable (append-only) de movimientos y transferencias de inventario."""

    tipo_movimiento = models.CharField(
        "tipo de movimiento", max_length=30, choices=TipoMovimientoStock.choices
    )
    lote_id = models.BigIntegerField("ID de lote", null=True, blank=True)
    producto_id = models.BigIntegerField(
        "ID de producto o material", null=True, blank=True
    )
    cantidad = models.DecimalField("cantidad", max_digits=12, decimal_places=4)
    codigo_um = models.CharField(
        "código unidad de medida", max_length=10, blank=True, default=""
    )
    local_origen = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="movimientos_stock_origen",
        verbose_name="local de origen",
    )
    local_destino = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="movimientos_stock_destino",
        verbose_name="local de destino",
    )
    usuario = models.ForeignKey(
        "core.Usuario",
        on_delete=models.PROTECT,
        related_name="movimientos_stock_auditados",
        verbose_name="usuario",
    )
    motivo = models.CharField("motivo", max_length=255, blank=True, default="")
    creado_en = models.DateTimeField("fecha y hora", auto_now_add=True)

    class Meta:
        verbose_name = "bitácora de stock"
        verbose_name_plural = "bitácoras de stock"
        db_table = "auditoria.bitacora_stock"
        ordering = ["-creado_en"]
        indexes = [
            models.Index(
                fields=["local_origen", "-creado_en"],
                name="audit_stk_loc_orig_idx",
            ),
            models.Index(
                fields=["producto_id", "-creado_en"],
                name="audit_stk_prod_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(tipo_movimiento__in=TipoMovimientoStock.values),
                name="audit_stock_tipo_ck",
            ),
        ]

    def __str__(self):
        return (
            f"[{self.creado_en:%Y-%m-%d %H:%M}] {self.tipo_movimiento} "
            f"({self.cantidad} {self.codigo_um})"
        )

    def save(self, *args, **kwargs):
        if self.pk:
            raise PermissionDenied(
                "Los registros de BitacoraStock son append-only y no pueden ser modificados."
            )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise PermissionDenied(
            "Los registros de BitacoraStock son append-only y no pueden ser eliminados."
        )
