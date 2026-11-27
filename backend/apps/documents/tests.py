"""Pruebas del módulo documentos."""

from django.test import TestCase

from backend.apps.core.models import Local, Usuario
from backend.apps.documents.choices import EstadoDocumento, TipoDocumento
from backend.apps.documents.models import Documento, PlantillaDocumento


class DocumentsModelsTest(TestCase):
    def setUp(self):
        self.local = Local.objects.create(codigo="L01", nombre="Local Principal")
        self.user = Usuario.objects.create_user(
            nombre_usuario="docuser",
            correo="docuser@example.com",
            password="securepassword",
        )
        self.plantilla = PlantillaDocumento.objects.create(
            codigo="PLANT-FAC-01",
            nombre="Factura Estándar",
            tipo=TipoDocumento.FACTURA,
            contenido_html="<h1>Factura {{ numero }}</h1>",
            version="1.0",
            es_predeterminada=True,
        )

    def test_crear_plantilla(self):
        self.assertEqual(str(self.plantilla), "PLANT-FAC-01 - Factura Estándar (v1.0)")
        self.assertTrue(self.plantilla.activo)
        self.assertTrue(self.plantilla.es_predeterminada)

    def test_crear_documento(self):
        doc = Documento.objects.create(
            correlativo="FAC-2026-000001",
            tipo_documento=TipoDocumento.FACTURA,
            local=self.local,
            anio=2026,
            plantilla=self.plantilla,
            entidad_tipo="sales_pedido_venta",
            entidad_id=100,
            generado_por=self.user,
            hash_seguridad="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            url_archivo="/media/documentos/2026/FAC-2026-000001.pdf",
            estado=EstadoDocumento.GENERADO,
        )
        self.assertEqual(str(doc), "factura FAC-2026-000001 (L01)")
        self.assertEqual(doc.estado, EstadoDocumento.GENERADO)
