"""Servicios para la matriz y cálculo de precios."""
from decimal import Decimal
from .models import ItemMatrizPrecios


def calcular_precio_final(precio_base: Decimal, margen: Decimal = Decimal("1.30"), iva: Decimal = Decimal("1.16")) -> Decimal:
    """Aplica la fórmula acordada (RF-45): precio final = base × 1.30 (margen) × 1.16 (IVA)."""
    return (precio_base * margen * iva).quantize(Decimal("0.01"))


def quote_price(producto_id=None, servicio_id=None, material_id=None, talla_id=None, medida=None):
    """Consulta la matriz de precios para cotizar un ítem."""
    # TODO: Resolver coincidencia exacta o por defecto en la matriz
    pass
