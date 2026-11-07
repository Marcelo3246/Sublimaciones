"""Servicios para el módulo de auditoría."""
from .models import BitacoraAccion, BitacoraStock


def registrar_accion(usuario, modulo, entidad, entidad_id, accion="modificar", estado_anterior=None, estado_nuevo=None, ip=None):
    """Registra un evento de acción de usuario en la bitácora append-only."""
    return BitacoraAccion.objects.create(
        usuario=usuario,
        modulo=modulo,
        entidad=entidad,
        entidad_id=entidad_id,
        accion=accion,
        estado_anterior=estado_anterior,
        estado_nuevo=estado_nuevo,
        direccion_ip=ip,
    )


def registrar_movimiento_stock(local, tipo_item, item_id, tipo_movimiento, cantidad, um, partida_id=None, usuario_id=None, motivo=""):
    """Registra un movimiento físico o contable de stock en la bitácora append-only."""
    return BitacoraStock.objects.create(
        local=local,
        tipo_item=tipo_item,
        item_id=item_id,
        tipo_movimiento=tipo_movimiento,
        partida_id=partida_id,
        usuario_id=usuario_id,
        cantidad=cantidad,
        um=um,
        motivo=motivo,
    )
