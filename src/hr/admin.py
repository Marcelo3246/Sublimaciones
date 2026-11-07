from django.contrib import admin
from .models import Trabajador, PeriodoPlanilla, Comision, Adelanto, PagoTrabajador

admin.site.register(Trabajador)
admin.site.register(PeriodoPlanilla)
admin.site.register(Comision)
admin.site.register(Adelanto)
admin.site.register(PagoTrabajador)
