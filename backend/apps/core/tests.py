"""Pruebas del módulo núcleo e identidad."""

from decimal import Decimal
from django.test import TestCase
from django.utils import timezone

from backend.apps.core.choices import TipoComprobante
from backend.apps.core.models import ContadorCorrelativo, Local, TasaCambio, Usuario


class CoreModelsTest(TestCase):
    def setUp(self):
        self.local = Local.objects.create(
            codigo="L01",
            nombre="Local Principal",
            persona_contacto="Admin Central",
        )
        self.user = Usuario.objects.create_user(
            nombre_usuario="testuser",
            correo="test@example.com",
            password="securepassword",
        )

    def test_crear_local(self):
        self.assertEqual(str(self.local), "L01 - Local Principal")
        self.assertEqual(self.local.persona_contacto, "Admin Central")

    def test_crear_usuario(self):
        self.assertTrue(self.user.check_password("securepassword"))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_tasa_cambio_y_obtener_vigente(self):
        tasa = TasaCambio.objects.create(
            fecha_vigencia=timezone.now().date(),
            dolares_a_bs=Decimal("36.5000"),
            registrado_por=self.user,
        )
        self.assertIn("36.5000", str(tasa))
        vigente = TasaCambio.obtener_vigente()
        self.assertIsNotNone(vigente)
        self.assertEqual(vigente.dolares_a_bs, Decimal("36.5000"))

    def test_contador_correlativo_obtener_siguiente(self):
        correlativo_1 = ContadorCorrelativo.obtener_siguiente(
            tipo_comprobante=TipoComprobante.FACTURA,
            local=self.local,
            anio=2026,
            prefijo="FAC",
        )
        self.assertEqual(correlativo_1, "FAC-2026-000001")

        correlativo_2 = ContadorCorrelativo.obtener_siguiente(
            tipo_comprobante=TipoComprobante.FACTURA,
            local=self.local,
            anio=2026,
            prefijo="FAC",
        )
        self.assertEqual(correlativo_2, "FAC-2026-000002")

        contador = ContadorCorrelativo.objects.get(
            tipo_comprobante=TipoComprobante.FACTURA,
            local=self.local,
            anio=2026,
        )
        self.assertEqual(contador.numero_actual, 2)
