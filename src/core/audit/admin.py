from django.contrib import admin
from .models import BitacoraAccion, BitacoraStock

@admin.register(BitacoraAccion)
class BitacoraAccionAdmin(admin.ModelAdmin):
    list_display = ("creado_en", "usuario", "modulo", "entidad", "entidad_id", "accion", "direccion_ip")
    list_filter = ("modulo", "accion")
    search_fields = ("entidad", "usuario__username")
    readonly_fields = [f.name for f in BitacoraAccion._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BitacoraStock)
class BitacoraStockAdmin(admin.ModelAdmin):
    list_display = ("creado_en", "local", "tipo_item", "tipo_movimiento", "cantidad", "um")
    list_filter = ("local", "tipo_item", "tipo_movimiento")
    search_fields = ("motivo",)
    readonly_fields = [f.name for f in BitacoraStock._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
