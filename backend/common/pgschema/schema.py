"""Editor de esquemas PostgreSQL con soporte de esquemas por módulo."""

from django.db.backends import utils as db_utils
from django.db.backends.ddl_references import Statement
from django.db.backends.postgresql.schema import (
    DatabaseSchemaEditor as PostgreSQLDatabaseSchemaEditor,
)


class DatabaseSchemaEditor(PostgreSQLDatabaseSchemaEditor):
    """Editor de Django corregido para ``Meta.db_table`` esquema-calificado.

    Los nombres auto-generados de índices y restricciones ya no llevan punto
    gracias al parche de ``backend.common.pgschema.split``; aquí se corrigen
    las dos operaciones que emiten SQL con el nombre de tabla como referencia.
    """

    def alter_db_table(self, model, old_db_table, new_db_table):
        """Renombra y/o mueve la tabla entre esquemas.

        ``ALTER TABLE ... RENAME TO`` no admite un destino cualificado y
        ``SET SCHEMA`` no cambia el nombre, así que las dos situaciones se
        resuelven combinando ambos.
        """
        if old_db_table == new_db_table or (
            self.connection.features.ignores_table_name_case
            and old_db_table.lower() == new_db_table.lower()
        ):
            return
        old_schema, old_name = db_utils.split_identifier(old_db_table)
        new_schema, new_name = db_utils.split_identifier(new_db_table)

        current_schema = old_schema
        if old_schema != new_schema:
            # Un esquema vacío equivale al esquema por defecto (public).
            current_schema = new_schema or "public"
            self.execute(
                "ALTER TABLE %s SET SCHEMA %s"
                % (
                    self.quote_name(old_db_table),
                    self.quote_name(current_schema),
                )
            )
        if old_name != new_name:
            current_table = (
                "%s.%s" % (current_schema, old_name) if current_schema else old_name
            )
            self.execute(
                self.sql_rename_table
                % {
                    "old_table": self.quote_name(current_table),
                    "new_table": self.quote_name(new_name),
                }
            )

        if self.collect_sql:
            # En ``migrate --sql`` el renombre no se ejecuta, así que hay que
            # redirigir la introspección posterior al nombre antiguo (igual
            # que hace el método original de Django).
            existing_table = self.collected_table_renames.pop(
                old_db_table, old_db_table
            )
            self.collected_table_renames[new_db_table] = existing_table
        # Renombrar todas las referencias diferidas a la tabla antigua.
        for sql in self.deferred_sql:
            if isinstance(sql, Statement):
                sql.rename_table_references(old_db_table, new_db_table)

    def _delete_fk_sql(self, model, name):
        """Borra una FK cualificando el ``SET CONSTRAINTS`` con el esquema.

        Django emite el nombre de la restricción desnudo y PostgreSQL solo lo
        resuelve contra las tablas del ``search_path``: con la tabla en
        ``ventas`` (fuera del ``search_path``) la restricción no aparece y la
        operación falla. ``ALTER TABLE ... DROP CONSTRAINT`` sí resuelve el
        nombre contra la tabla indicada, así que solo califica el primer
        comando.
        """
        table = model._meta.db_table
        schema, _ = db_utils.split_identifier(table)
        constraint = "%s.%s" % (schema, name) if schema else name
        return (
            "SET CONSTRAINTS %s IMMEDIATE; ALTER TABLE %s DROP CONSTRAINT %s"
            % (
                self.quote_name(constraint),
                self.quote_name(table),
                self.quote_name(name),
            )
        )
