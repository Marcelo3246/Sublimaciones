"""Administración de Django para el módulo ventas."""

from django.contrib import admin

from backend.apps.sales.models import (
    Cliente,
    Cobro,
    Factura,
    LineaPedido,
    PedidoVenta,
)


class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido
    extra = 0


class CobroInline(admin.TabularInline):
    model = Cobro
    extra = 0


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "rif", "telefono", "correo", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre", "rif", "correo", "telefono")


@admin.register(PedidoVenta)
class PedidoVentaAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "cliente",
        "local",
        "estado",
        "moneda",
        "total",
        "vendedor",
        "fecha_compromiso",
        "creado_en",
    )
    list_filter = ("estado", "local", "moneda")
    search_fields = ("codigo", "cliente__nombre", "cliente__rif")
    inlines = (LineaPedidoInline, CobroInline)


@admin.register(LineaPedido)
class LineaPedidoAdmin(admin.ModelAdmin):
    list_display = (
        "pedido_venta",
        "tipo_linea",
        "variante",
        "servicio",
        "cantidad",
        "precio_unitario",
        "moneda",
    )
    list_filter = ("tipo_linea", "moneda")
    search_fields = ("pedido_venta__codigo", "variante__sku", "servicio__nombre")


@admin.register(Cobro)
class CobroAdmin(admin.ModelAdmin):
    list_display = (
        "pedido_venta",
        "monto",
        "moneda",
        "metodo",
        "referencia",
        "tasa_aplicada",
        "fecha",
        "activo",
    )
    list_filter = ("metodo", "moneda", "activo")
    search_fields = ("pedido_venta__codigo", "referencia")


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = (
        "numero",
        "anio",
        "tipo",
        "local",
        "pedido_venta",
        "estado",
        "total",
        "moneda",
        "fecha_emision",
        "emitida_por",
    )
    list_filter = ("tipo", "estado", "local", "anio")
    search_fields = ("numero", "pedido_venta__codigo")
