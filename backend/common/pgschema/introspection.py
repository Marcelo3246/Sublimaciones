"""Introspección de PostgreSQL con nombres de tabla esquema-calificados."""

from django.db.backends import utils as db_utils
from django.db.backends.postgresql.introspection import (
    DatabaseIntrospection as PostgreSQLDatabaseIntrospection,
    FieldInfo,
    TableInfo,
    psycopg_version,
)
from django.db.models import Index

# Filtro de esquemas del catálogo que no pertenecen a la base de datos de la
# aplicación (pg_catalog, pg_toast, pg_temp_*, information_schema).
_NON_APP_SCHEMAS_SQL = """
    AND n.nspname NOT IN ('information_schema')
    AND n.nspname !~ '^pg_'
"""


def _regclass_ref(table_name):
    """Referencia de relación apta para ``to_regclass()``.

    Acepta ``nucleo.usuario`` o ``usuario`` y devuelve cada tramo
    entrecomillado (``"nucleo"."usuario"``), de modo que la resolución no
    dependa del ``search_path`` cuando el nombre ya trae esquema.
    """
    schema, name = db_utils.split_identifier(table_name)
    if schema:
        return '"%s"."%s"' % (schema.replace('"', '""'), name.replace('"', '""'))
    return '"%s"' % name.replace('"', '""')


class DatabaseIntrospection(PostgreSQLDatabaseIntrospection):
    """Introspección de Django sin el filtro ``pg_table_is_visible``.

    El filtro original solo ve las tablas del ``search_path`` y compara por
    ``relname`` desnudo, de modo que con esquemas por módulo no encontraría
    ``nucleo.usuario`` ni distinguiría dos tablas homónimas. Aquí se devuelven
    nombres calificados (``esquema.tabla``, salvo ``public``) y se resuelve
    la tabla con ``to_regclass()``.
    """

    def get_table_list(self, cursor):
        """Devuelve todas las tablas y vistas, esquema-calificadas.

        Las tablas de ``public`` (auth, django_*) se devuelven sin esquema
        porque sus modelos declaran ``db_table`` desnudo y Django compara los
        nombres por igualdad exacta (p. ej. ``MigrationRecorder.has_table``).
        """
        cursor.execute(
            """
            SELECT
                CASE
                    WHEN n.nspname = 'public' THEN c.relname
                    ELSE n.nspname || '.' || c.relname
                END,
                CASE
                    WHEN c.relispartition THEN 'p'
                    WHEN c.relkind IN ('m', 'v') THEN 'v'
                    ELSE 't'
                END,
                obj_description(c.oid, 'pg_class')
            FROM pg_catalog.pg_class c
            JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind IN ('f', 'm', 'p', 'r', 'v')
            """
            + _NON_APP_SCHEMAS_SQL
        )
        return [
            TableInfo(*row)
            for row in cursor.fetchall()
            if row[0] not in self.ignored_tables
        ]

    def get_table_description(self, cursor, table_name):
        """Describe las columnas de ``table_name`` (acepta esquema)."""
        cursor.execute(
            """
            SELECT
                a.attname AS column_name,
                NOT (a.attnotnull OR (t.typtype = 'd' AND t.typnotnull)) AS is_nullable,
                pg_get_expr(ad.adbin, ad.adrelid) AS column_default,
                CASE WHEN collname = 'default' THEN NULL ELSE collname END AS collation,
                a.attidentity != '' AS is_autofield,
                col_description(a.attrelid, a.attnum) AS column_comment
            FROM pg_attribute a
            LEFT JOIN pg_attrdef ad ON a.attrelid = ad.adrelid AND a.attnum = ad.adnum
            LEFT JOIN pg_collation co ON a.attcollation = co.oid
            JOIN pg_type t ON a.atttypid = t.oid
            JOIN pg_class c ON a.attrelid = c.oid
            JOIN pg_namespace n ON c.relnamespace = n.oid
            WHERE c.relkind IN ('f', 'm', 'p', 'r', 'v')
                AND c.oid = to_regclass(%s)
            """
            + _NON_APP_SCHEMAS_SQL,
            [_regclass_ref(table_name)],
        )
        field_map = {line[0]: line[1:] for line in cursor.fetchall()}
        cursor.execute(
            "SELECT * FROM %s LIMIT 1" % self.connection.ops.quote_name(table_name)
        )

        # PostgreSQL OIDs may vary depending on the installation, especially
        # for datatypes from extensions, e.g. "hstore". The type_display
        # attribute (psycopg 3.2+) should be used.
        type_display_available = psycopg_version() >= (3, 2)
        return [
            FieldInfo(
                line.name,
                (
                    line.type_display
                    if type_display_available and line.type_display == "hstore"
                    else line.type_code
                ),
                # display_size is always None on psycopg2.
                line.internal_size if line.display_size is None else line.display_size,
                line.internal_size,
                # precision is always None for non-numeric types on psycopg2,
                # and for numeric types it's 2**16 - 1 when the precision is
                # unknown.
                None if line.precision == 2**16 - 1 else line.precision,
                None if line.scale == 2**16 - 1 else line.scale,
                *field_map[line.name],
            )
            for line in cursor.description
        ]

    def get_sequences(self, cursor, table_name, table_fields=()):
        """Secuencias de ``table_name`` con nombre esquema-calificado.

        El nombre se califica porque ``_get_sequence_name`` lo usa en
        ``DROP SEQUENCE``/``ALTER SEQUENCE``, que sí dependen del
        ``search_path``.
        """
        cursor.execute(
            """
            SELECT
                n.nspname || '.' || s.relname AS sequence_name,
                a.attname AS colname
            FROM
                pg_class s
                JOIN pg_namespace n ON n.oid = s.relnamespace
                JOIN pg_depend d ON d.objid = s.oid
                    AND d.classid = 'pg_class'::regclass
                    AND d.refclassid = 'pg_class'::regclass
                JOIN pg_attribute a ON d.refobjid = a.attrelid
                    AND d.refobjsubid = a.attnum
                JOIN pg_class tbl ON tbl.oid = d.refobjid
                    AND tbl.oid = to_regclass(%s)
            WHERE
                s.relkind = 'S';
        """,
            [_regclass_ref(table_name)],
        )
        return [
            {"name": row[0], "table": table_name, "column": row[1]}
            for row in cursor.fetchall()
        ]

    def get_relations(self, cursor, table_name):
        """Foreign keys de ``table_name`` como ``{column: (otra_col, otra_tabla, on_delete)}``.

        Se admite el caso entre esquemas (``ventas.cliente`` ->
        ``nucleo.local``), que la condición original de mismo esquema descartaba.
        """
        cursor.execute(
            """
            SELECT a1.attname, c2.relname, a2.attname, con.confdeltype
            FROM pg_constraint con
            LEFT JOIN pg_class c1 ON con.conrelid = c1.oid
            LEFT JOIN pg_class c2 ON con.confrelid = c2.oid
            LEFT JOIN
                pg_attribute a1 ON c1.oid = a1.attrelid AND a1.attnum = con.conkey[1]
            LEFT JOIN
                pg_attribute a2 ON c2.oid = a2.attrelid AND a2.attnum = con.confkey[1]
            WHERE
                c1.oid = to_regclass(%s) AND
                con.contype = 'f'
        """,
            [_regclass_ref(table_name)],
        )
        return {
            row[0]: (row[2], row[1], self.on_delete_types.get(row[3]))
            for row in cursor.fetchall()
        }

    def get_constraints(self, cursor, table_name):
        """Restricciones e índices de ``table_name`` (acepta esquema)."""
        constraints = {}
        cursor.execute(
            """
            SELECT
                c.conname,
                array(
                    SELECT attname
                    FROM unnest(c.conkey) WITH ORDINALITY cols(colid, arridx)
                    JOIN pg_attribute AS ca ON cols.colid = ca.attnum
                    WHERE ca.attrelid = c.conrelid
                    ORDER BY cols.arridx
                ),
                c.contype,
                (SELECT fkc.relname || '.' || fka.attname
                FROM pg_attribute AS fka
                JOIN pg_class AS fkc ON fka.attrelid = fkc.oid
                WHERE fka.attrelid = c.confrelid AND fka.attnum = c.confkey[1]),
                cl.reloptions
            FROM pg_constraint AS c
            JOIN pg_class AS cl ON c.conrelid = cl.oid
            WHERE cl.oid = to_regclass(%s)
                AND c.contype != 'n'
        """,
            [_regclass_ref(table_name)],
        )
        for constraint, columns, kind, used_cols, options in cursor.fetchall():
            constraints[constraint] = {
                "columns": columns,
                "primary_key": kind == "p",
                "unique": kind in ["p", "u"],
                "foreign_key": tuple(used_cols.split(".", 1)) if kind == "f" else None,
                "check": kind == "c",
                "index": False,
                "definition": None,
                "options": options,
            }
        # Now get indexes
        cursor.execute(
            """
            SELECT
                indexname,
                array_agg(attname ORDER BY arridx),
                indisunique,
                indisprimary,
                array_agg(ordering ORDER BY arridx),
                amname,
                exprdef,
                s2.attoptions
            FROM (
                SELECT
                    c2.relname as indexname, idx.*, attr.attname, am.amname,
                    CASE
                        WHEN idx.indexprs IS NOT NULL THEN
                            pg_get_indexdef(idx.indexrelid)
                    END AS exprdef,
                    CASE am.amname
                        WHEN %s THEN
                            CASE (option & 1)
                                WHEN 1 THEN 'DESC' ELSE 'ASC'
                            END
                    END as ordering,
                    c2.reloptions as attoptions
                FROM (
                    SELECT *
                    FROM
                        pg_index i,
                        unnest(i.indkey, i.indoption)
                            WITH ORDINALITY koi(key, option, arridx)
                ) idx
                LEFT JOIN pg_class c ON idx.indrelid = c.oid
                LEFT JOIN pg_class c2 ON idx.indexrelid = c2.oid
                LEFT JOIN pg_am am ON c2.relam = am.oid
                LEFT JOIN
                    pg_attribute attr ON attr.attrelid = c.oid AND attr.attnum = idx.key
                WHERE c.oid = to_regclass(%s)
            ) s2
            GROUP BY indexname, indisunique, indisprimary, amname, exprdef, attoptions;
        """,
            [self.index_default_access_method, _regclass_ref(table_name)],
        )
        for (
            index,
            columns,
            unique,
            primary,
            orders,
            type_,
            definition,
            options,
        ) in cursor.fetchall():
            if index not in constraints:
                basic_index = (
                    type_ == self.index_default_access_method
                    and
                    # '_btree' references
                    # django.contrib.postgres.indexes.BTreeIndex.suffix.
                    not index.endswith("_btree")
                    and options is None
                )
                constraints[index] = {
                    "columns": columns if columns != [None] else [],
                    "orders": orders if orders != [None] else [],
                    "primary_key": primary,
                    "unique": unique,
                    "foreign_key": None,
                    "check": False,
                    "index": True,
                    "type": Index.suffix if basic_index else type_,
                    "definition": definition,
                    "options": options,
                }
        return constraints
