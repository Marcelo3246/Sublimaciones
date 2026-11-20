"""Administración de Django para el módulo recursos humanos."""

from django.contrib import admin

from backend.apps.hr.models import Trabajador, TrabajadorLocal


class TrabajadorLocalInline(admin.TabularInline):
    model = TrabajadorLocal
    extra = 0


@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_completo",
        "cargo",
        "telefono",
        "correo",
        "fecha_ingreso",
        "usuario",
        "activo",
    )
    list_filter = ("cargo", "activo")
    search_fields = ("nombre_completo", "correo", "telefono")
    inlines = (TrabajadorLocalInline,)


@admin.register(TrabajadorLocal)
class TrabajadorLocalAdmin(admin.ModelAdmin):
    list_display = ("trabajador", "local", "es_principal", "activo")
    list_filter = ("local", "es_principal", "activo")
    search_fields = ("trabajador__nombre_completo",)
