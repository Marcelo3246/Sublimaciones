"""Administración de Django para el módulo producción."""

from django.contrib import admin

from backend.apps.production.models import (
    ConsumoMaterial,
    Maquina,
    OperacionMaquina,
    OrdenProduccion,
    PasoProduccion,
)


@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "local", "tipo", "estado", "horas_operativas")
    list_filter = ("tipo", "estado", "local")
    search_fields = ("codigo", "nombre", "local__codigo", "local__nombre")


class ConsumoMaterialInline(admin.TabularInline):
    model = ConsumoMaterial
    extra = 0


class OperacionMaquinaInline(admin.TabularInline):
    model = OperacionMaquina
    extra = 0


class PasoProduccionInline(admin.TabularInline):
    model = PasoProduccion
    extra = 0
    show_change_link = True


@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "variante",
        "cantidad",
        "local_origen",
        "estado",
        "fecha_limite",
        "costo_total",
        "moneda",
    )
    list_filter = ("estado", "moneda", "local_origen")
    search_fields = ("codigo", "variante__sku", "variante__producto__nombre")
    inlines = (PasoProduccionInline,)


@admin.register(PasoProduccion)
class PasoProduccionAdmin(admin.ModelAdmin):
    list_display = (
        "orden_produccion",
        "orden_paso",
        "tipo",
        "local",
        "trabajador",
        "estado",
        "iniciado_en",
        "terminado_en",
    )
    list_filter = ("estado", "tipo", "local")
    search_fields = ("orden_produccion__codigo", "local__codigo")
    inlines = (ConsumoMaterialInline, OperacionMaquinaInline)


@admin.register(ConsumoMaterial)
class ConsumoMaterialAdmin(admin.ModelAdmin):
    list_display = (
        "paso",
        "lote",
        "stock",
        "cantidad_consumida",
        "unidad_medida",
        "tipo",
        "motivo_desperdicio",
    )
    list_filter = ("tipo",)
    search_fields = ("paso__orden_produccion__codigo", "lote__numero_lote")


@admin.register(OperacionMaquina)
class OperacionMaquinaAdmin(admin.ModelAdmin):
    list_display = (
        "maquina",
        "paso",
        "operador_trabajador",
        "duracion_minutos",
        "resultado",
        "creado_en",
    )
    list_filter = ("resultado", "maquina")
    search_fields = ("maquina__codigo", "maquina__nombre", "paso__orden_produccion__codigo")
