from django.contrib import admin
from .models import Categoria, Subcategoria, UnidadMedida, Talla, Material, Producto, VarianteProducto, Servicio, Diseno

admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(UnidadMedida)
admin.site.register(Talla)
admin.site.register(Material)
admin.site.register(Producto)
admin.site.register(VarianteProducto)
admin.site.register(Servicio)
admin.site.register(Diseno)
