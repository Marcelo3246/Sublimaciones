from django.contrib import admin
from .models import Proveedor, OrdenCompra, LineaOrdenCompra, FacturaCompra, HistorialPrecioProveedor

admin.site.register(Proveedor)
admin.site.register(OrdenCompra)
admin.site.register(LineaOrdenCompra)
admin.site.register(FacturaCompra)
admin.site.register(HistorialPrecioProveedor)
