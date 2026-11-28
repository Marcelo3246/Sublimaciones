"""Administración de Django para el módulo inventario."""

from django.contrib import admin

from backend.apps.inventory.models import (
    GuiaTransferencia,
    LineaGuiaTransferencia,
    Lote,
    MovimientoStock,
    NivelMinimo,
    Stock,
)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        "local",
        "variante",
        "material",
        "cantidad_disponible",
        "cantidad_reservada",
        "actualizado_en",
    )
    list_filter = ("local",)
    search_fields = (
        "local__codigo",
        "material__nombre",
        "material__codigo",
        "variante__sku",
    )


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = (
        "numero_lote",
        "material",
        "local",
        "longitud_actual",
        "costo_unitario",
        "moneda",
        "fecha_vencimiento",
        "activo",
    )
    list_filter = ("moneda", "local", "activo")
    search_fields = ("numero_lote", "material__nombre", "material__codigo")


@admin.register(MovimientoStock)
class MovimientoStockAdmin(admin.ModelAdmin):
    list_display = ("creado_en", "tipo", "local", "cantidad", "referencia")
    list_filter = ("tipo", "local")
    search_fields = ("referencia", "local__codigo", "local__nombre")


@admin.register(GuiaTransferencia)
class GuiaTransferenciaAdmin(admin.ModelAdmin):
    list_display = (
        "codigo_guia",
        "local_origen",
        "local_destino",
        "estado",
        "creado_en",
    )
    list_filter = ("estado", "local_origen", "local_destino")
    search_fields = ("codigo_guia",)


@admin.register(LineaGuiaTransferencia)
class LineaGuiaTransferenciaAdmin(admin.ModelAdmin):
    list_display = ("guia", "lote", "variante", "cantidad", "unidad_medida", "estado")
    list_filter = ("estado", "guia")
    search_fields = ("guia__codigo_guia", "variante__sku", "lote__numero_lote")


@admin.register(NivelMinimo)
class NivelMinimoAdmin(admin.ModelAdmin):
    list_display = ("local", "producto", "material", "cantidad_minima_alerta")
    list_filter = ("local",)
    search_fields = (
        "producto__nombre",
        "producto__codigo",
        "material__nombre",
        "material__codigo",
    )
