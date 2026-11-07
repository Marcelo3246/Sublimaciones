"""Servicios para RRHH y comisiones."""
from decimal import Decimal
from .models import Comision, Trabajador


def accumul_commission(worker_id: int, sale_id: int, pct: Decimal, total_sale: Decimal):
    """Acumula la comisión de un trabajador por una venta liquidada (RF-49)."""
    monto = (total_sale * pct).quantize(Decimal("0.01"))
    return Comision.objects.create(
        trabajador_id=worker_id,
        pedido_venta_id=sale_id,
        porcentaje_comision=pct,
        monto_comision=monto,
    )


def liquidar_periodo(periodo_id: int):
    """Liquida las comisiones de un período descontando adelantos (RF-50)."""
    # TODO: Implementar consolidación de pagos netos
    pass
