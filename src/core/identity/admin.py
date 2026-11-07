from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.identity.models import Local, Usuario


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "telefono", "activo", "creado_en")
    list_filter = ("activo",)
    search_fields = ("codigo", "nombre")
    ordering = ("codigo",)


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Admin del modelo Usuario personalizado.

    Extiende UserAdmin de Django para mantener la funcionalidad estándar
    (cambio de contraseña, permisos de Django, etc.) y agrega los campos
    propios del negocio.
    """

    list_display = (
        "username",
        "get_full_name",
        "es_global",
        "local_predeterminado",
        "is_active",
        "activo",
    )
    list_filter = ("es_global", "is_active", "activo")
    # Agregar campos propios a los fieldsets de UserAdmin
    fieldsets = UserAdmin.fieldsets + (
        (
            "DLL Sublimados",
            {
                "fields": ("es_global", "local_predeterminado", "activo"),
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "DLL Sublimados",
            {
                "fields": ("es_global", "local_predeterminado"),
            },
        ),
    )
