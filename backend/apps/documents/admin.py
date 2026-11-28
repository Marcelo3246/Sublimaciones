"""Administración de Django para el módulo documentos."""

from django.contrib import admin

from backend.apps.documents.models import Documento, PlantillaDocumento


@admin.register(PlantillaDocumento)
class PlantillaDocumentoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre",
        "tipo",
        "version",
        "es_predeterminada",
        "activo",
        "actualizado_en",
    )
    list_filter = ("tipo", "es_predeterminada", "activo")
    search_fields = ("codigo", "nombre")


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = (
        "correlativo",
        "tipo_documento",
        "local",
        "anio",
        "estado",
        "generado_por",
        "fecha_emision",
    )
    list_filter = ("tipo_documento", "estado", "local", "anio")
    search_fields = (
        "correlativo",
        "entidad_tipo",
        "generado_por__nombre_usuario",
        "local__codigo",
    )
    readonly_fields = (
        "correlativo",
        "tipo_documento",
        "local",
        "anio",
        "plantilla",
        "entidad_tipo",
        "entidad_id",
        "generado_por",
        "fecha_emision",
        "hash_seguridad",
        "url_archivo",
        "creado_en",
        "actualizado_en",
    )
