"""Servicios expuestos por el módulo de catálogo."""
from .models import Producto, Material, Diseno


def get_product_spec(product_id: int):
    """Obtiene las especificaciones de un producto para la orden de producción."""
    return Producto.objects.filter(id=product_id, activo=True).first()
