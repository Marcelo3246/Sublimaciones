"""Administración de Django para el módulo catálogo."""

from django.contrib import admin

from backend.apps.catalog.models import (
    Categoria,
    Material,
    Producto,
    Servicio,
    Subcategoria,
    Talla,
    UnidadMedida,
    VarianteProducto,
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "activo", "creado_en")
    list_filter = ("tipo", "activo")
    search_fields = ("nombre",)


@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "activo", "creado_en")
    list_filter = ("categoria", "activo")
    search_fields = ("nombre", "categoria__nombre")


@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "permite_decimales", "creado_en")
    list_filter = ("permite_decimales",)
    search_fields = ("codigo", "nombre")


@admin.register(Talla)
class TallaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "orden", "creado_en")
    list_filter = ("codigo",)
    search_fields = ("codigo", "nombre")
    ordering = ("orden", "codigo")


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre",
        "categoria",
        "unidad_medida",
        "es_continuo",
        "stock_minimo_global",
        "activo",
    )
    list_filter = ("es_continuo", "categoria", "activo")
    search_fields = ("codigo", "nombre")


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "subcategoria", "tipo", "activo")
    list_filter = ("tipo", "subcategoria", "activo")
    search_fields = ("codigo", "nombre", "descripcion")


@admin.register(VarianteProducto)
class VarianteProductoAdmin(admin.ModelAdmin):
    list_display = ("sku", "producto", "talla", "color", "codigo_barras", "activo")
    list_filter = ("producto", "talla", "activo")
    search_fields = ("sku", "codigo_barras", "color", "producto__nombre")


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "unidad_medida", "activo", "creado_en")
    list_filter = ("unidad_medida", "activo")
    search_fields = ("nombre", "descripcion")
