"""Administración de Django para el módulo auditoría."""

from django.contrib import admin

from backend.apps.audit.models import BitacoraAccion, BitacoraStock


@admin.register(BitacoraAccion)
class BitacoraAccionAdmin(admin.ModelAdmin):
    list_display = (
        "creado_en",
        "usuario",
        "local",
        "modulo",
        "accion",
        "entidad",
        "entidad_id",
        "ip_origen",
    )
    list_filter = ("accion", "modulo", "local")
    search_fields = (
        "usuario__nombre_usuario",
        "entidad",
        "ip_origen",
        "modulo",
    )
    readonly_fields = [f.name for f in BitacoraAccion._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BitacoraStock)
class BitacoraStockAdmin(admin.ModelAdmin):
    list_display = (
        "creado_en",
        "tipo_movimiento",
        "cantidad",
        "codigo_um",
        "local_origen",
        "local_destino",
        "usuario",
        "motivo",
    )
    list_filter = ("tipo_movimiento", "local_origen", "local_destino")
    search_fields = ("usuario__nombre_usuario", "motivo", "codigo_um")
    readonly_fields = [f.name for f in BitacoraStock._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
