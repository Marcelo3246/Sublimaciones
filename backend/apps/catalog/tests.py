"""Pruebas del módulo catálogo."""

from decimal import Decimal

from django.test import TestCase

from backend.apps.catalog.choices import TipoCategoria, TipoProducto
from backend.apps.catalog.models import (
    Categoria,
    Material,
    Producto,
    Servicio,
    Subcategoria,
    Talla,
    UnidadMedida,
    VarianteProducto,
)


class CatalogModelsTest(TestCase):
    """Pruebas de creación de los modelos del catálogo maestro."""

    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre="Telas Textiles",
            tipo=TipoCategoria.MATERIAL,
        )
        self.subcategoria = Subcategoria.objects.create(
            categoria=self.categoria,
            nombre="Microdurazno",
        )
        self.unidad = UnidadMedida.objects.create(
            codigo="m",
            nombre="Metros",
            permite_decimales=True,
        )
        self.talla = Talla.objects.create(codigo="M", nombre="Mediana", orden=3)
        self.material = Material.objects.create(
            codigo="MAT-001",
            nombre="Rollo Microdurazno Blanco",
            categoria=self.categoria,
            unidad_medida=self.unidad,
            es_continuo=True,
            stock_minimo_global=Decimal("10.0000"),
        )
        self.producto = Producto.objects.create(
            codigo="PRO-001",
            nombre="Franela Deportiva",
            subcategoria=self.subcategoria,
            tipo=TipoProducto.TERMINADO,
        )
        self.variante = VarianteProducto.objects.create(
            producto=self.producto,
            talla=self.talla,
            color="Blanco",
            sku="FRA-M-BLA",
        )

    def test_crear_categoria(self):
        self.assertEqual(str(self.categoria), "Telas Textiles (Material)")
        self.assertTrue(self.categoria.activo)

    def test_crear_subcategoria(self):
        self.assertEqual(str(self.subcategoria), "Microdurazno (Telas Textiles)")
        self.assertEqual(self.subcategoria.categoria, self.categoria)

    def test_crear_unidad_medida(self):
        self.assertEqual(str(self.unidad), "m - Metros")
        self.assertTrue(self.unidad.permite_decimales)

    def test_crear_talla(self):
        self.assertEqual(str(self.talla), "M - Mediana")
        self.assertEqual(self.talla.orden, 3)

    def test_crear_material_continuo(self):
        self.assertEqual(str(self.material), "MAT-001 - Rollo Microdurazno Blanco")
        self.assertTrue(self.material.es_continuo)
        self.assertEqual(self.material.stock_minimo_global, Decimal("10.0000"))

    def test_crear_producto(self):
        self.assertEqual(str(self.producto), "PRO-001 - Franela Deportiva")
        self.assertEqual(self.producto.tipo, TipoProducto.TERMINADO)
        self.assertEqual(self.producto.subcategoria, self.subcategoria)

    def test_crear_variante(self):
        self.assertEqual(str(self.variante), "FRA-M-BLA - Franela Deportiva")
        self.assertEqual(self.variante.talla, self.talla)
        self.variante.refresh_from_db()
        self.assertTrue(self.variante.activo)

    def test_variante_sin_talla(self):
        unica = VarianteProducto.objects.create(
            producto=self.producto,
            color="Negro",
            sku="FRA-UNI-NEG",
        )
        self.assertIsNone(unica.talla)

    def test_crear_servicio(self):
        servicio = Servicio.objects.create(
            nombre="Sublimación por metro",
            descripcion="Servicio de sublimación por metro lineal",
            unidad_medida=self.unidad,
        )
        self.assertEqual(str(servicio), "Sublimación por metro")
        self.assertEqual(servicio.unidad_medida, self.unidad)
