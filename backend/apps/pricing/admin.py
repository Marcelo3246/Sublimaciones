"""Administración de Django para el módulo precios."""

from django.contrib import admin

from backend.apps.pricing.models import (
    HistorialCambioPrecio,
    ItemMatrizPrecios,
    ParametroFormula,
)


@admin.register(ItemMatrizPrecios)
class ItemMatrizPreciosAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "producto",
        "variante",
        "servicio",
        "material",
        "precio_base",
        "moneda",
        "porcentaje_margen",
        "porcentaje_iva",
        "activo",
    )
    list_filter = ("moneda", "activo")
    search_fields = ("producto__nombre", "variante__sku", "servicio__nombre")


@admin.register(HistorialCambioPrecio)
class HistorialCambioPrecioAdmin(admin.ModelAdmin):
    list_display = (
        "item_matriz",
        "precio_anterior",
        "precio_nuevo",
        "usuario",
        "cambiado_en",
    )
    list_filter = ("cambiado_en",)
    readonly_fields = (
        "item_matriz",
        "precio_anterior",
        "precio_nuevo",
        "usuario",
        "cambiado_en",
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ParametroFormula)
class ParametroFormulaAdmin(admin.ModelAdmin):
    list_display = (
        "porcentaje_margen",
        "porcentaje_iva",
        "fecha_desde",
        "fecha_hasta",
        "registrado_por",
        "activo",
    )
    list_filter = ("activo",)
    ordering = ("-fecha_desde",)
