"""Pruebas del módulo producción."""

from decimal import Decimal

from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from backend.apps.catalog.models import (
    Categoria,
    Material,
    Producto,
    Talla,
    UnidadMedida,
    VarianteProducto,
)
from backend.apps.core.models import Local
from backend.apps.hr.choices import CargoTrabajador
from backend.apps.hr.models import Trabajador
from backend.apps.inventory.models import Lote
from backend.apps.production.choices import (
    EstadoMaquina,
    EstadoOrdenProduccion,
    EstadoPasoProduccion,
    ResultadoOperacion,
    TipoConsumo,
    TipoMaquina,
    TipoPaso,
)
from backend.apps.production.models import (
    ConsumoMaterial,
    Maquina,
    OperacionMaquina,
    OrdenProduccion,
    PasoProduccion,
)


class ProductionModelTest(TestCase):
    def setUp(self):
        self.local = Local.objects.create(codigo="L01", nombre="Sede Central")
        self.local_2 = Local.objects.create(codigo="L02", nombre="Sucursal 2")
        self.um = UnidadMedida.objects.create(codigo="m", nombre="Metro")
        self.cat = Categoria.objects.create(nombre="Textiles")
        self.material = Material.objects.create(
            codigo="MAT-001",
            nombre="Rollo Microdurazno",
            categoria=self.cat,
            unidad_medida=self.um,
            es_continuo=True,
        )
        self.lote = Lote.objects.create(
            material=self.material,
            local=self.local,
            numero_lote="LOTE-001",
            longitud_inicial=Decimal("50.0000"),
            longitud_actual=Decimal("50.0000"),
            costo_unitario=Decimal("15.00"),
        )
        self.prod = Producto.objects.create(codigo="PROD-001", nombre="Franela")
        self.talla = Talla.objects.create(codigo="M", nombre="Mediana", orden=1)
        self.variante = VarianteProducto.objects.create(
            producto=self.prod,
            talla=self.talla,
            sku="FRANELA-M",
        )
        self.trabajador = Trabajador.objects.create(
            nombre_completo="Juan Operario",
            cargo=CargoTrabajador.IMPRESOR,
        )
        self.maquina = Maquina.objects.create(
            codigo="MQ-001",
            nombre="Plóter Mimaki",
            local=self.local,
            tipo=TipoMaquina.IMPRESORA,
            estado=EstadoMaquina.OPERATIVA,
        )

    def test_crear_maquina_y_estado(self):
        self.assertTrue(self.maquina.activo)
        self.assertEqual(self.maquina.horas_operativas, Decimal("0"))
        self.assertEqual(str(self.maquina), f"MQ-001 - Plóter Mimaki ({self.local.codigo})")

    def test_orden_produccion_cierre_costo_constraint(self):
        # Orden terminada sin costo_total ni fecha_cierre debe fallar (RF-35)
        with self.assertRaises(IntegrityError), transaction.atomic():
            OrdenProduccion.objects.create(
                codigo="OP-FAIL",
                variante=self.variante,
                cantidad=Decimal("10.0000"),
                local_origen=self.local,
                estado=EstadoOrdenProduccion.TERMINADA,
            )

        # Con costo_total y fecha_cierre debe crearse exitosamente
        op = OrdenProduccion.objects.create(
            codigo="OP-OK",
            variante=self.variante,
            cantidad=Decimal("10.0000"),
            local_origen=self.local,
            estado=EstadoOrdenProduccion.TERMINADA,
            costo_total=Decimal("150.00"),
            fecha_cierre=timezone.now(),
        )
        self.assertEqual(op.estado, EstadoOrdenProduccion.TERMINADA)

    def test_paso_produccion_secuencia(self):
        op = OrdenProduccion.objects.create(
            codigo="OP-RUTA",
            variante=self.variante,
            cantidad=Decimal("5.0000"),
            local_origen=self.local,
            estado=EstadoOrdenProduccion.EN_PRODUCCION,
        )
        PasoProduccion.objects.create(
            orden_produccion=op,
            orden_paso=1,
            tipo=TipoPaso.IMPRESION,
            local=self.local,
            estado=EstadoPasoProduccion.TERMINADO,
        )
        PasoProduccion.objects.create(
            orden_produccion=op,
            orden_paso=2,
            tipo=TipoPaso.CONFECCION,
            local=self.local_2,
            estado=EstadoPasoProduccion.PENDIENTE,
        )
        self.assertEqual(op.pasos.count(), 2)

        # Repetir orden_paso en la misma orden debe fallar por UniqueConstraint
        with self.assertRaises(IntegrityError), transaction.atomic():
            PasoProduccion.objects.create(
                orden_produccion=op,
                orden_paso=1,
                tipo=TipoPaso.CORTE,
                local=self.local,
            )

    def test_consumo_material_exclusion_mutua(self):
        op = OrdenProduccion.objects.create(
            codigo="OP-CONS",
            variante=self.variante,
            cantidad=Decimal("2.0000"),
            local_origen=self.local,
        )
        paso = PasoProduccion.objects.create(
            orden_produccion=op,
            orden_paso=1,
            local=self.local,
        )
        # Consumo sin lote ni stock debe fallar
        with self.assertRaises(IntegrityError), transaction.atomic():
            ConsumoMaterial.objects.create(
                paso=paso,
                cantidad_consumida=Decimal("1.5000"),
                unidad_medida=self.um,
            )

        # Consumo con lote físico exitoso
        consumo = ConsumoMaterial.objects.create(
            paso=paso,
            lote=self.lote,
            cantidad_consumida=Decimal("1.5000"),
            unidad_medida=self.um,
            tipo=TipoConsumo.USO,
        )
        self.assertTrue(consumo.activo)
        self.assertIsNotNone(consumo.creado_en)
        self.assertIsNotNone(consumo.actualizado_en)

    def test_consumo_material_desperdicio_motivo_obligatorio(self):
        op = OrdenProduccion.objects.create(
            codigo="OP-DESP",
            variante=self.variante,
            cantidad=Decimal("2.0000"),
            local_origen=self.local,
        )
        paso = PasoProduccion.objects.create(
            orden_produccion=op,
            orden_paso=1,
            local=self.local,
        )
        # Desperdicio sin motivo debe fallar (RF-34)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ConsumoMaterial.objects.create(
                paso=paso,
                lote=self.lote,
                cantidad_consumida=Decimal("0.5000"),
                unidad_medida=self.um,
                tipo=TipoConsumo.DESPERDICIO,
                motivo_desperdicio="",
            )

        # Con motivo debe crearse
        consumo = ConsumoMaterial.objects.create(
            paso=paso,
            lote=self.lote,
            cantidad_consumida=Decimal("0.5000"),
            unidad_medida=self.um,
            tipo=TipoConsumo.DESPERDICIO,
            motivo_desperdicio="Error de corte en cabezal",
        )
        self.assertEqual(consumo.tipo, TipoConsumo.DESPERDICIO)

    def test_operacion_maquina(self):
        op = OrdenProduccion.objects.create(
            codigo="OP-MAQ",
            variante=self.variante,
            cantidad=Decimal("10.0000"),
            local_origen=self.local,
        )
        paso = PasoProduccion.objects.create(
            orden_produccion=op,
            orden_paso=1,
            local=self.local,
        )
        operacion = OperacionMaquina.objects.create(
            paso=paso,
            maquina=self.maquina,
            operador_trabajador=self.trabajador,
            duracion_minutos=Decimal("45.50"),
            resultado=ResultadoOperacion.COMPLETADO,
        )
        self.assertEqual(operacion.duracion_minutos, Decimal("45.50"))
        self.assertEqual(paso.operaciones_maquina.count(), 1)
