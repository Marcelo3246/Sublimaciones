"""Servicios para producción multi-local."""
from .models import OrdenProduccion, PasoProduccion, ConsumoMaterial


def crear_orden_desde_pedido(pedido_id: int):
    """Crea una orden de producción con ruta de pasos según el pedido (RF-30, RF-31)."""
    # TODO: Implementar generación de pasos multi-local
    pass


def registrar_consumo_material(paso_id, partida_id, cantidad, tipo_consumo="uso", motivo=""):
    """Registra consumo de material por medición (RF-32) o desperdicio (RF-34)."""
    # TODO: Integrar con inventory.services.consume_material
    pass


def finalizar_orden_produccion(orden_id: int):
    """Al completar la orden, genera entrada del producto terminado en el local final (RF-35)."""
    # TODO: Alimentar stock terminado
    pass
