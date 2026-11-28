"""Pruebas del módulo compras."""

from decimal import Decimal

from django.db import IntegrityError, transaction
from django.test import TestCase

from backend.apps.catalog.models import Categoria, Material, UnidadMedida
from backend.apps.core.models import Local, TasaCambio, Usuario
from backend.apps.purchasing.choices import EstadoOrdenCompra, Moneda
from backend.apps.purchasing.models import (
    Empresa,
    FacturaCompra,
    HistorialPrecioProveedor,
    LineaOrdenCompra,
    LineaRecepcionCompra,
    OrdenCompra,
    Proveedor,
    RecepcionCompra,
)


class PurchasingModelTest(TestCase):
    def setUp(self):
        self.local = Local.objects.create(codigo="L01", nombre="Sede Central")
        self.usuario = Usuario.objects.create_user(
            nombre_usuario="admin", correo="admin@example.com", password="x"
        )
        self.um = UnidadMedida.objects.create(codigo="m", nombre="Metro")
        self.cat = Categoria.objects.create(nombre="Textiles")
        self.material = Material.objects.create(
            codigo="MAT-001",
            nombre="Rollo Microdurazno",
            categoria=self.cat,
            unidad_medida=self.um,
            es_continuo=True,
        )
        self.empresa = Empresa.objects.create(
            nombre="Distribuidora Textil del Lago, C.A.",
            rif="J-30123456-7",
        )
        self.proveedor = Proveedor.objects.create(
            empresa=self.empresa,
            persona_contacto="María González",
            calificacion=5,
        )

    def test_crear_empresa_y_proveedor(self):
        self.assertTrue(self.empresa.activo)
        self.assertEqual(self.empresa.proveedores.count(), 1)
        self.assertEqual(self.proveedor.moneda_predeterminada, Moneda.USD)
        self.assertEqual(str(self.proveedor), f"María González ({self.empresa.nombre})")

    def test_calificacion_proveedor_rango(self):
        # Calificación inválida mayor a 5 debe fallar por CheckConstraint
        with self.assertRaises(IntegrityError), transaction.atomic():
            Proveedor.objects.create(
                empresa=self.empresa,
                persona_contacto="Contacto Inválido",
                calificacion=6,
            )

    def test_orden_compra_y_lineas(self):
        orden = OrdenCompra.objects.create(
            numero_orden="OC-0001",
            proveedor=self.proveedor,
            local=self.local,
            estado=EstadoOrdenCompra.BORRADOR,
            total=Decimal("450.00"),
            moneda=Moneda.USD,
        )
        linea = LineaOrdenCompra.objects.create(
            orden_compra=orden,
            material=self.material,
            unidad_medida=self.um,
            cantidad_solicitada=Decimal("10.0000"),
            cantidad_recibida=Decimal("0.0000"),
            precio_unitario=Decimal("45.00"),
            moneda=Moneda.USD,
        )
        self.assertEqual(orden.lineas.count(), 1)
        self.assertEqual(linea.cantidad_solicitada, Decimal("10.0000"))

    def test_linea_orden_recibida_no_excede_solicitada(self):
        orden = OrdenCompra.objects.create(
            numero_orden="OC-0002",
            proveedor=self.proveedor,
            local=self.local,
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            LineaOrdenCompra.objects.create(
                orden_compra=orden,
                material=self.material,
                unidad_medida=self.um,
                cantidad_solicitada=Decimal("5.0000"),
                cantidad_recibida=Decimal("6.0000"),
                precio_unitario=Decimal("10.00"),
            )

    def test_recepcion_compra_y_linea(self):
        orden = OrdenCompra.objects.create(
            numero_orden="OC-0003",
            proveedor=self.proveedor,
            local=self.local,
        )
        linea_oc = LineaOrdenCompra.objects.create(
            orden_compra=orden,
            material=self.material,
            unidad_medida=self.um,
            cantidad_solicitada=Decimal("10.0000"),
            precio_unitario=Decimal("20.00"),
        )
        recepcion = RecepcionCompra.objects.create(
            orden_compra=orden,
            local=self.local,
            numero_guia_proveedor="GUIA-1234",
        )
        linea_rec = LineaRecepcionCompra.objects.create(
            recepcion_compra=recepcion,
            linea_orden_compra=linea_oc,
            cantidad_recibida=Decimal("10.0000"),
            unidad_medida=self.um,
        )
        self.assertEqual(recepcion.lineas.count(), 1)
        self.assertEqual(linea_rec.cantidad_recibida, Decimal("10.0000"))

    def test_factura_compra_con_tasa(self):
        tasa = TasaCambio.objects.create(
            dolares_a_bs=Decimal("60.5000"),
            registrado_por=self.usuario,
        )
        factura = FacturaCompra.objects.create(
            proveedor=self.proveedor,
            numero_externo="FAC-9999",
            total=Decimal("6050.00"),
            moneda=Moneda.VES,
            tasa_aplicada=tasa,
        )
        self.assertEqual(factura.tasa_aplicada.dolares_a_bs, Decimal("60.5000"))

    def test_historial_precio_proveedor(self):
        historial = HistorialPrecioProveedor.objects.create(
            proveedor=self.proveedor,
            empresa=self.empresa,
            material=self.material,
            unidad_medida=self.um,
            precio_unitario=Decimal("45.00"),
            moneda=Moneda.USD,
        )
        self.assertIsNotNone(historial.registrado_en)
        self.assertEqual(historial.precio_unitario, Decimal("45.00"))
