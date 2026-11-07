"""Servicios de compras."""
from .models import HistorialPrecioProveedor, OrdenCompra


def comparar_precios_proveedor(material_id: int):
    """Compara precios históricos por material y proveedor (RF-28)."""
    return HistorialPrecioProveedor.objects.filter(material_id=material_id, activo=True).order_by("precio_unitario")


def registrar_recepcion_compra(orden_id: int):
    """Al recibir la compra, alimenta el inventario del local receptor."""
    # TODO: Generar entradas de stock y partidas correspondientes
    pass
