"""Pruebas unitarias del backend ``backend.common.pgschema``.

No tocan la base de datos: el editor de esquemas trabaja en modo
``collect_sql`` (solo acumula el SQL) y el resto son funciones puras.
"""

from django.db import connection
from django.db.backends import utils as db_utils
from django.db.backends.base import schema as base_schema
from django.db.models import indexes as indexes_module
from django.test import SimpleTestCase

from backend.apps.sales.models import Cliente, PedidoVenta
from backend.common.pgschema import split_identifier
from backend.common.pgschema.operations import DatabaseOperations


class SplitIdentifierTest(SimpleTestCase):
    """Partición de identificadores con esquema."""

    def test_parte_esquema_sin_comillas(self):
        self.assertEqual(split_identifier("nucleo.usuario"), ("nucleo", "usuario"))

    def test_identificador_sin_esquema(self):
        self.assertEqual(split_identifier("usuario"), ("", "usuario"))

    def test_identificador_entrecomillado(self):
        self.assertEqual(
            split_identifier('"nucleo"."usuario"'), ("nucleo", "usuario")
        )

    def test_parche_instalado_en_django(self):
        # Los tres módulos que importan la función deben usar la variante
        # propia; sin el parche los nombres auto-generados llevarían punto.
        for module in (db_utils, base_schema, indexes_module):
            self.assertIs(module.split_identifier, split_identifier)


class QuoteNameTest(SimpleTestCase):
    """Cita de identificadores esquema-calificados."""

    def setUp(self):
        self.quote_name = connection.ops.quote_name

    def test_el_motor_es_el_backend_propio(self):
        self.assertIsInstance(connection.ops, DatabaseOperations)

    def test_nombre_con_esquema(self):
        self.assertEqual(self.quote_name("nucleo.usuario"), '"nucleo"."usuario"')

    def test_nombre_sin_esquema(self):
        self.assertEqual(self.quote_name("usuario"), '"usuario"')

    def test_nombre_ya_partido(self):
        self.assertEqual(
            self.quote_name('"nucleo"."usuario"'), '"nucleo"."usuario"'
        )


class SchemaEditorTest(SimpleTestCase):
    """SQL generado por el editor de esquemas (sin ejecutarlo)."""

    # El editor abre un ``atomic`` al entrar; se permite la conexión aunque
    # las pruebas no consulten datos.
    databases = {"default"}

    def _collect_alter(self, old_db_table, new_db_table):
        with connection.schema_editor(collect_sql=True) as editor:
            editor.alter_db_table(Cliente, old_db_table, new_db_table)
        return editor.collected_sql

    def test_renombrar_en_el_mismo_esquema(self):
        sql = self._collect_alter("ventas.cliente", "ventas.cliente_nueva")
        self.assertEqual(len(sql), 1)
        # RENAME TO no admite destino cualificado: el nombre va desnudo.
        self.assertIn('ALTER TABLE "ventas"."cliente" RENAME TO', sql[0])
        self.assertIn('"cliente_nueva"', sql[0])

    def test_mover_de_esquema_con_renombre(self):
        sql = self._collect_alter("ventas.cliente", "nucleo.cliente_nueva")
        self.assertEqual(len(sql), 2)
        self.assertIn('ALTER TABLE "ventas"."cliente" SET SCHEMA "nucleo"', sql[0])
        self.assertIn('ALTER TABLE "nucleo"."cliente" RENAME TO', sql[1])

    def test_mover_de_esquema_sin_renombre(self):
        sql = self._collect_alter("ventas.cliente", "nucleo.cliente")
        self.assertEqual(len(sql), 1)
        self.assertIn('SET SCHEMA "nucleo"', sql[0])

    def test_borrado_de_fk_califica_set_constraints(self):
        with connection.schema_editor(collect_sql=True) as editor:
            sql = editor._delete_fk_sql(
                Cliente, "cliente_id_1a2b3c4d_fk_pedido_venta_id"
            )
        # SET CONSTRAINTS resuelve el nombre contra el search_path: fuera de
        # él hay que indicar el esquema de la tabla dueña de la restricción.
        self.assertTrue(sql.startswith('SET CONSTRAINTS "ventas"."'), sql)
        self.assertIn('ALTER TABLE "ventas"."cliente" DROP CONSTRAINT', sql)

    def test_nombre_de_indice_sin_punto(self):
        with connection.schema_editor(collect_sql=True) as editor:
            name = editor._create_index_name("ventas.cliente", ["nombre"])
        self.assertNotIn(".", name)
        self.assertTrue(name.startswith("cliente_nombre_"), name)

    def test_nombre_de_fk_sin_punto_ni_esquema(self):
        with connection.schema_editor(collect_sql=True) as editor:
            name = str(
                editor._fk_constraint_name(
                    PedidoVenta,
                    PedidoVenta._meta.get_field("cliente"),
                    "_fk_%(to_table)s_%(to_column)s",
                )
            )
        # El nombre llega entrecomillado y sin el esquema de la tabla
        # referenciada (ventas.cliente -> cliente).
        bare = name.strip('"')
        self.assertNotIn(".", bare)
        self.assertTrue(bare.endswith("_fk_cliente_id"), bare)
