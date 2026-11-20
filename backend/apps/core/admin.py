"""Administración de Django para el núcleo del sistema."""

from django.contrib import admin

from backend.apps.core.models import (
    ContadorCorrelativo,
    Local,
    TasaCambio,
    Usuario,
)


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre",
        "telefono",
        "persona_contacto",
        "activo",
        "creado_en",
    )
    list_filter = ("activo",)
    search_fields = ("codigo", "nombre", "persona_contacto")


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_usuario",
        "correo",
        "rol",
        "local",
        "es_global",
        "activo",
        "creado_en",
    )
    list_filter = ("rol", "es_global", "activo", "local")
    search_fields = ("nombre_usuario", "correo", "nombre", "apellido")


@admin.register(TasaCambio)
class TasaCambioAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_vigencia",
        "dolares_a_bs",
        "registrado_por",
        "activo",
        "creado_en",
    )
    list_filter = ("activo", "fecha_vigencia")
    search_fields = ("registrado_por__nombre_usuario", "registrado_por__correo")


@admin.register(ContadorCorrelativo)
class ContadorCorrelativoAdmin(admin.ModelAdmin):
    list_display = (
        "tipo_comprobante",
        "local",
        "anio",
        "prefijo",
        "numero_actual",
        "activo",
        "actualizado_en",
    )
    list_filter = ("tipo_comprobante", "local", "anio", "activo")
    search_fields = ("tipo_comprobante", "prefijo", "local__nombre", "local__codigo")
