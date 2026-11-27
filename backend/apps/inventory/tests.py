"""Pruebas del módulo inventario."""

from decimal import Decimal

from django.test import TestCase

from backend.apps.catalog.choices import TipoCategoria
from backend.apps.catalog.models import (
    Categoria,
    Material,
    Producto,
    UnidadMedida,
    VarianteProducto,
)
from backend.apps.core.models import Local
from backend.apps.inventory.choices import (
    EstadoGuiaTransferencia,
    TipoMovimiento,
)
from backend.apps.inventory.models import (
    GuiaTransferencia,
    LineaGuiaTransferencia,
    Lote,
    MovimientoStock,
    NivelMinimo,
    Stock,
)


class InventoryModelsTest(TestCase):
    """Pruebas de creación de los modelos de inventario multi-local."""

    def setUp(self):
        self.local = Local.objects.create(
            codigo="L01",
            nombre="Local Principal",
        )
        self.local_destino = Local.objects.create(
            codigo="L02",
            nombre="Local 2",
        )
        self.categoria = Categoria.objects.create(
            nombre="Viniles",
            tipo=TipoCategoria.MATERIAL,
        )
        self.unidad = UnidadMedida.objects.create(
            codigo="rollo",
            nombre="Rollos",
            permite_decimales=False,
        )
        self.material = Material.objects.create(
            codigo="VIN-001",
            nombre="Vinil Textil Poliuretano",
            categoria=self.categoria,
            unidad_medida=self.unidad,
            es_continuo=True,
        )
        self.producto = Producto.objects.create(
            codigo="PRO-001",
            nombre="Taza Blanca 11oz",
        )
        self.variante = VarianteProducto.objects.create(
            producto=self.producto,
            color="Blanco",
            sku="TAZ-11OZ-BLA",
        )
        self.lote = Lote.objects.create(
            material=self.material,
            local=self.local,
            numero_lote="LOT-2026-0001",
            longitud_inicial=Decimal("50.0000"),
            longitud_actual=Decimal("35.5000"),
            costo_unitario=Decimal("42.50"),
        )

    def test_crear_stock_material(self):
        stock = Stock.objects.create(
            local=self.local,
            material=self.material,
            cantidad_disponible=Decimal("35.5000"),
        )
        self.assertIn("L01", str(stock))
        self.assertEqual(stock.cantidad_reservada, Decimal("0.0000"))
        self.assertTrue(stock.activo)

    def test_crear_stock_variante(self):
        stock = Stock.objects.create(
            local=self.local,
            variante=self.variante,
            cantidad_disponible=Decimal("12.0000"),
            cantidad_reservada=Decimal("2.0000"),
        )
        self.assertIn("TAZ-11OZ-BLA", str(stock))
        self.assertEqual(stock.cantidad_reservada, Decimal("2.0000"))

    def test_crear_lote(self):
        self.assertEqual(str(self.lote), "LOT-2026-0001 - VIN-001")
        self.assertEqual(self.lote.moneda, "USD")
        self.assertIsNotNone(self.lote.fecha_ingreso)

    def test_crear_movimiento_stock(self):
        movimiento = MovimientoStock.objects.create(
            tipo=TipoMovimiento.ENTRADA,
            local=self.local,
            cantidad=Decimal("10.0000"),
            referencia="OC-0001",
        )
        self.assertIn("ENTRADA", str(movimiento))
        self.assertEqual(movimiento.referencia, "OC-0001")

    def test_crear_guia_transferencia_con_linea(self):
        guia = GuiaTransferencia.objects.create(
            codigo_guia="GUIA-2026-0001",
            local_origen=self.local,
            local_destino=self.local_destino,
            estado=EstadoGuiaTransferencia.EN_TRANSITO,
        )
        self.assertIn("En tránsito", str(guia))

        linea = LineaGuiaTransferencia.objects.create(
            guia=guia,
            lote=self.lote,
            cantidad=Decimal("10.0000"),
            unidad_medida=self.unidad,
        )
        self.assertIn("GUIA-2026-0001", str(linea))
        self.assertEqual(guia.lineas.count(), 1)
        self.assertEqual(linea.estado, "PENDIENTE")

    def test_crear_nivel_minimo(self):
        nivel = NivelMinimo.objects.create(
            local=self.local,
            material=self.material,
            cantidad_minima_alerta=Decimal("5.0000"),
        )
        self.assertIn("VIN-001", str(nivel))
        self.assertEqual(nivel.cantidad_minima_alerta, Decimal("5.0000"))

    def test_nivel_minimo_producto(self):
        nivel = NivelMinimo.objects.create(
            local=self.local,
            producto=self.producto,
            cantidad_minima_alerta=Decimal("3.0000"),
        )
        self.assertIn("Taza Blanca 11oz", str(nivel))
