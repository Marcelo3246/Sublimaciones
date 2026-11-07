from django.contrib import admin
from .models import Maquina, OrdenProduccion, PasoProduccion, ConsumoMaterial, OperacionMaquina

admin.site.register(Maquina)
admin.site.register(OrdenProduccion)
admin.site.register(PasoProduccion)
admin.site.register(ConsumoMaterial)
admin.site.register(OperacionMaquina)
