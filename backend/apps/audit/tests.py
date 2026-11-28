"""Pruebas del módulo auditoría."""

from decimal import Decimal
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from backend.apps.audit.choices import AccionAuditoria, TipoMovimientoStock
from backend.apps.audit.models import BitacoraAccion, BitacoraStock
from backend.apps.core.models import Local, Usuario


class AuditModelsTest(TestCase):
    def setUp(self):
        self.local = Local.objects.create(codigo="L01", nombre="Local Principal")
        self.user = Usuario.objects.create_user(
            nombre_usuario="audituser",
            correo="audit@example.com",
            password="securepassword",
        )

    def test_crear_bitacora_accion(self):
        accion = BitacoraAccion.objects.create(
            usuario=self.user,
            local=self.local,
            modulo="catalog",
            accion=AccionAuditoria.INSERT,
            entidad="catalog_producto",
            entidad_id=1,
            datos_despues={"nombre": "Taza Blanca"},
            ip_origen="127.0.0.1",
        )
        self.assertIn("audituser", str(accion))
        self.assertIn("INSERT", str(accion))

        # Comprobar inmutabilidad append-only
        with self.assertRaises(PermissionDenied):
            accion.entidad = "catalog_material"
            accion.save()

        with self.assertRaises(PermissionDenied):
            accion.delete()

    def test_crear_bitacora_stock(self):
        stock_mov = BitacoraStock.objects.create(
            tipo_movimiento=TipoMovimientoStock.ENTRADA,
            producto_id=10,
            cantidad=Decimal("50.0000"),
            codigo_um="m",
            local_origen=self.local,
            usuario=self.user,
            motivo="Recepción de compra",
        )
        self.assertIn("ENTRADA", str(stock_mov))
        self.assertIn("50.0000", str(stock_mov))

        # Comprobar inmutabilidad append-only
        with self.assertRaises(PermissionDenied):
            stock_mov.cantidad = Decimal("60.0000")
            stock_mov.save()

        with self.assertRaises(PermissionDenied):
            stock_mov.delete()
