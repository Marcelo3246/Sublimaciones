"""Pruebas del módulo recursos humanos."""

from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from backend.apps.core.models import Local
from backend.apps.hr.choices import CargoTrabajador
from backend.apps.hr.models import Trabajador, TrabajadorLocal


class TrabajadorModelTest(TestCase):
    def setUp(self):
        self.local = Local.objects.create(codigo="L01", nombre="Sede Central")
        self.local_2 = Local.objects.create(codigo="L02", nombre="Sucursal 2")
        self.trabajador = Trabajador.objects.create(
            nombre_completo="Ana Pérez",
            cargo=CargoTrabajador.VENDEDOR,
        )

    def test_crear_trabajador_con_valores_por_defecto(self):
        self.assertTrue(self.trabajador.activo)
        self.assertIsNone(self.trabajador.usuario)
        self.assertEqual(self.trabajador.fecha_ingreso, timezone.localdate())

    def test_asignacion_multi_local(self):
        TrabajadorLocal.objects.create(
            trabajador=self.trabajador, local=self.local, es_principal=True
        )
        TrabajadorLocal.objects.create(trabajador=self.trabajador, local=self.local_2)
        self.assertEqual(self.trabajador.asignaciones.count(), 2)

    def test_no_repite_local(self):
        TrabajadorLocal.objects.create(trabajador=self.trabajador, local=self.local)
        with self.assertRaises(IntegrityError), transaction.atomic():
            TrabajadorLocal.objects.create(trabajador=self.trabajador, local=self.local)

    def test_un_solo_local_principal(self):
        TrabajadorLocal.objects.create(
            trabajador=self.trabajador, local=self.local, es_principal=True
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            TrabajadorLocal.objects.create(
                trabajador=self.trabajador, local=self.local_2, es_principal=True
            )
