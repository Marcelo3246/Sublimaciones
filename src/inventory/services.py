"""Servicios de inventario expuestos para otros módulos."""
from django.db import transaction
from .models import Existencia, Partida, MovimientoStock, GuiaTransferencia


def reserve_stock(order_line):
    """Reserva stock para una línea de pedido o producción."""
    # TODO: Implementar lógica de reserva
    pass


def discount_for_sale(order_line):
    """Descuenta existencias del local al emitir factura o nota de entrega."""
    # TODO: Implementar descuento de inventario
    pass


def consume_material(partida_id, measured_qty):
    """Registra consumo de material por medición sobre una partida/rollo."""
    # TODO: Descontar de partida y verificar si sobrante < sobrante_minimo para marcar desperdicio
    pass


def receive_transfer(guide_id):
    """Confirma recepción de una transferencia entre locales y alimenta el stock destino."""
    # TODO: Implementar confirmación de guía
    pass
