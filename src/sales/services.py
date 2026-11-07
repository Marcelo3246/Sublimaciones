"""Servicios para el módulo de ventas."""
from django.db import transaction
from .models import PedidoVenta, LineaPedido, Factura


def crear_pedido(cliente_id, local_id, lineas_data, moneda="USD"):
    """Crea un pedido con sus líneas respectivas."""
    # TODO: Implementar cálculo y snapshot de precios
    pass


def confirmar_pedido(pedido_id):
    """Cambia estado a 'confirmado' y genera orden de producción si aplica."""
    # TODO: Integrar con production
    pass


def emitir_factura(pedido_id, usuario_id):
    """Emite factura propia descontando existencias (RF-40)."""
    # TODO: Integrar con inventory y documents
    pass


def anular_pedido(pedido_id, motivo=""):
    """Anula pedido y revierte stock reservado (RF-43)."""
    pass
