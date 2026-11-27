"""Pruebas del módulo precios."""

from datetime import date
from decimal import Decimal

from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction
from django.test import TestCase

from backend.apps.catalog.models import Producto, Servicio, UnidadMedida
from backend.apps.core.models import Usuario
from backend.apps.pricing.models import (
    HistorialCambioPrecio,
    ItemMatrizPrecios,
    ParametroFormula,
)


class PricingModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            nombre_usuario="admin", correo="admin@example.com", password="x"
        )
        self.producto = Producto.objects.create(codigo="P-TAZA", nombre="Taza 11oz")
        self.servicio = Servicio.objects.create(nombre="Sublimación por metro")
        self.oz = UnidadMedida.objects.create(codigo="OZ", nombre="Onza")
        self.base = {
            "precio_base": Decimal("5.00"),
            "porcentaje_margen": Decimal("1.3000"),
            "porcentaje_iva": Decimal("0.1600"),
        }

    def test_item_de_producto_con_medida(self):
        item = ItemMatrizPrecios.objects.create(
            producto=self.producto,
            medida_cantidad=Decimal("11"),
            unidad_medida_medida=self.oz,
            **self.base,
        )
        self.assertEqual(item.moneda, "USD")

    def test_destinos_excluyentes(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            ItemMatrizPrecios.objects.create(
                producto=self.producto, servicio=self.servicio, **self.base
            )
        with self.assertRaises(IntegrityError), transaction.atomic():
            ItemMatrizPrecios.objects.create(**self.base)

    def test_medida_requiere_unidad(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            ItemMatrizPrecios.objects.create(
                servicio=self.servicio, medida_cantidad=Decimal("1"), **self.base
            )

    def test_historial_es_append_only(self):
        item = ItemMatrizPrecios.objects.create(servicio=self.servicio, **self.base)
        cambio = HistorialCambioPrecio.objects.create(
            item_matriz=item,
            precio_anterior=Decimal("5.00"),
            precio_nuevo=Decimal("6.00"),
            usuario=self.usuario,
        )
        with self.assertRaises(PermissionDenied):
            cambio.save()
        with self.assertRaises(PermissionDenied):
            cambio.delete()

    def test_parametro_formula_vigencia(self):
        ParametroFormula.objects.create(
            porcentaje_margen=Decimal("1.3000"),
            porcentaje_iva=Decimal("0.1600"),
            fecha_desde=date(2026, 1, 1),
            registrado_por=self.usuario,
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            ParametroFormula.objects.create(
                porcentaje_margen=Decimal("1.3000"),
                porcentaje_iva=Decimal("0.1600"),
                fecha_desde=date(2026, 1, 1),
                registrado_por=self.usuario,
            )
        with self.assertRaises(IntegrityError), transaction.atomic():
            ParametroFormula.objects.create(
                porcentaje_margen=Decimal("1.3000"),
                porcentaje_iva=Decimal("0.1600"),
                fecha_desde=date(2026, 6, 1),
                fecha_hasta=date(2026, 5, 1),
                registrado_por=self.usuario,
            )
