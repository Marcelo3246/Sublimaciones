from django.contrib import admin
from .models import Existencia, Partida, MovimientoStock, GuiaTransferencia

admin.site.register(Existencia)
admin.site.register(Partida)
admin.site.register(MovimientoStock)
admin.site.register(GuiaTransferencia)
