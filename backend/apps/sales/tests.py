"""Pruebas del módulo ventas."""

from decimal import Decimal

from django.db import IntegrityError, transaction
from django.test import TestCase

from backend.apps.catalog.models import (
    Categoria,
    Material,
    Producto,
    Servicio,
    UnidadMedida,
    VarianteProducto,
)
from backend.apps.core.models import Local, TasaCambio, Usuario
from backend.apps.sales.choices import (
    EstadoFactura,
    EstadoPedido,
    MetodoCobro,
    TipoLineaPedido,
)
from backend.apps.sales.models import Cliente, Cobro, Factura, LineaPedido, PedidoVenta


class SalesModelTest(TestCase):
    def setUp(self):
        self.local = Local.objects.create(codigo="L01", nombre="Sede Central")
        self.usuario = Usuario.objects.create_user(
            nombre_usuario="vendedor", correo="v@example.com", password="x"
        )
        self.cliente = Cliente.objects.create(nombre="Consumidor Final")
        self.pedido = PedidoVenta.objects.create(
            codigo="PV-000001", cliente=self.cliente, local=self.local
        )
        producto = Producto.objects.create(codigo="P-FRA", nombre="Franela")
        self.variante = VarianteProducto.objects.create(producto=producto, sku="FRA-M")
        self.servicio = Servicio.objects.create(nombre="Sublimación por metro")
        unidad = UnidadMedida.objects.create(codigo="M", nombre="Metro")
        categoria = Categoria.objects.create(nombre="Telas")
        self.material = Material.objects.create(
            codigo="TEL-01",
            nombre="Tela poliéster",
            categoria=categoria,
            unidad_medida=unidad,
        )

    def test_pedido_por_defecto_cotizado(self):
        self.assertEqual(self.pedido.estado, EstadoPedido.COTIZADO)
        self.assertIsNone(self.pedido.vendedor)

    def test_anular_exige_motivo(self):
        self.pedido.estado = EstadoPedido.ANULADO
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.pedido.save()
        self.pedido.motivo_anulacion = "Cliente desistió"
        self.pedido.save()

    def test_coherencia_tipo_linea(self):
        LineaPedido.objects.create(
            pedido_venta=self.pedido,
            variante=self.variante,
            cantidad=Decimal("2"),
            precio_unitario=Decimal("10.00"),
        )
        LineaPedido.objects.create(
            pedido_venta=self.pedido,
            tipo_linea=TipoLineaPedido.SERVICIO_PURO,
            servicio=self.servicio,
            cantidad=Decimal("1.5"),
            precio_unitario=Decimal("4.00"),
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            LineaPedido.objects.create(
                pedido_venta=self.pedido,
                tipo_linea=TipoLineaPedido.SERVICIO_PURO,
                cantidad=Decimal("1"),
                precio_unitario=Decimal("4.00"),
            )
        with self.assertRaises(IntegrityError), transaction.atomic():
            LineaPedido.objects.create(
                pedido_venta=self.pedido,
                tipo_linea=TipoLineaPedido.PRODUCTO_PERSONALIZADO,
                variante=self.variante,
                cantidad=Decimal("1"),
                precio_unitario=Decimal("12.00"),
            )
        LineaPedido.objects.create(
            pedido_venta=self.pedido,
            tipo_linea=TipoLineaPedido.PRODUCTO_PERSONALIZADO,
            variante=self.variante,
            material=self.material,
            cantidad=Decimal("1"),
            precio_unitario=Decimal("12.00"),
        )
        self.assertEqual(self.pedido.lineas.count(), 3)

    def test_cobro_en_bs_exige_tasa(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Cobro.objects.create(
                pedido_venta=self.pedido,
                monto=Decimal("400.00"),
                moneda="VES",
                metodo=MetodoCobro.PUNTO,
            )
        tasa = TasaCambio.objects.create(dolares_a_bs=Decimal("40.0000"))
        Cobro.objects.create(
            pedido_venta=self.pedido,
            monto=Decimal("400.00"),
            moneda="VES",
            metodo=MetodoCobro.PUNTO,
            tasa_aplicada=tasa,
        )
        Cobro.objects.create(
            pedido_venta=self.pedido,
            monto=Decimal("5.00"),
            metodo=MetodoCobro.DIVISA,
        )
        self.assertEqual(self.pedido.cobros.count(), 2)

    def test_factura_correlativo_y_anulacion(self):
        datos = {
            "pedido_venta": self.pedido,
            "local": self.local,
            "numero": "000001",
            "anio": 2026,
            "total": Decimal("20.00"),
            "emitida_por": self.usuario,
        }
        factura = Factura.objects.create(**datos)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Factura.objects.create(**datos)
        factura.estado = EstadoFactura.ANULADA
        with self.assertRaises(IntegrityError), transaction.atomic():
            factura.save()
