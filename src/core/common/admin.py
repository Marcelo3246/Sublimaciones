from django.contrib import admin

from core.common.models import TasaCambio


@admin.register(TasaCambio)
class TasaCambioAdmin(admin.ModelAdmin):
    list_display = ("fecha_vigencia", "dolares_a_bs", "registrado_por", "creado_en")
    list_filter = ("fecha_vigencia",)
    search_fields = ("fecha_vigencia",)
    ordering = ("-fecha_vigencia",)
