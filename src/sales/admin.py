from django.contrib import admin
from .models import Cliente, PedidoVenta, LineaPedido, Factura

admin.site.register(Cliente)
admin.site.register(PedidoVenta)
admin.site.register(LineaPedido)
admin.site.register(Factura)
