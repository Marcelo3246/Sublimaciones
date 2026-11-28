"""Administración de Django para el módulo compras."""

from django.contrib import admin

from backend.apps.purchasing.models import (
    Empresa,
    FacturaCompra,
    HistorialPrecioProveedor,
    LineaOrdenCompra,
    LineaRecepcionCompra,
    OrdenCompra,
    Proveedor,
    RecepcionCompra,
)


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("rif", "nombre", "telefono", "correo", "activo")
    list_filter = ("activo",)
    search_fields = ("rif", "nombre", "correo")


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = (
        "persona_contacto",
        "empresa",
        "telefono",
        "moneda_predeterminada",
        "calificacion",
        "activo",
    )
    list_filter = ("moneda_predeterminada", "empresa", "activo")
    search_fields = ("persona_contacto", "correo", "empresa__nombre", "empresa__rif")


class LineaOrdenCompraInline(admin.TabularInline):
    model = LineaOrdenCompra
    extra = 0


@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = (
        "numero_orden",
        "proveedor",
        "local",
        "estado",
        "total",
        "moneda",
        "fecha_emision",
    )
    list_filter = ("estado", "moneda", "local")
    search_fields = ("numero_orden", "proveedor__persona_contacto", "proveedor__empresa__nombre")
    inlines = (LineaOrdenCompraInline,)


class LineaRecepcionCompraInline(admin.TabularInline):
    model = LineaRecepcionCompra
    extra = 0


@admin.register(RecepcionCompra)
class RecepcionCompraAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "orden_compra",
        "local",
        "estado",
        "fecha_recepcion",
        "numero_guia_proveedor",
    )
    list_filter = ("estado", "local")
    search_fields = ("orden_compra__numero_orden", "numero_guia_proveedor")
    inlines = (LineaRecepcionCompraInline,)


@admin.register(LineaOrdenCompra)
class LineaOrdenCompraAdmin(admin.ModelAdmin):
    list_display = (
        "orden_compra",
        "material",
        "cantidad_solicitada",
        "cantidad_recibida",
        "precio_unitario",
        "moneda",
    )
    list_filter = ("moneda",)
    search_fields = ("orden_compra__numero_orden", "material__nombre", "material__codigo")


@admin.register(LineaRecepcionCompra)
class LineaRecepcionCompraAdmin(admin.ModelAdmin):
    list_display = (
        "recepcion_compra",
        "linea_orden_compra",
        "cantidad_recibida",
        "unidad_medida",
        "lote",
    )
    search_fields = ("recepcion_compra__id", "linea_orden_compra__material__nombre")


@admin.register(FacturaCompra)
class FacturaCompraAdmin(admin.ModelAdmin):
    list_display = (
        "numero_externo",
        "proveedor",
        "fecha_emision",
        "total",
        "moneda",
        "tasa_aplicada",
    )
    list_filter = ("moneda", "fecha_emision")
    search_fields = ("numero_externo", "proveedor__persona_contacto", "proveedor__empresa__nombre")


@admin.register(HistorialPrecioProveedor)
class HistorialPrecioProveedorAdmin(admin.ModelAdmin):
    list_display = (
        "material",
        "proveedor",
        "precio_unitario",
        "moneda",
        "registrado_en",
    )
    list_filter = ("moneda",)
    search_fields = ("material__nombre", "material__codigo", "proveedor__persona_contacto")
    readonly_fields = ("registrado_en",)
