"""``quote_name`` con soporte de esquemas."""

from django.db.backends.postgresql.operations import (
    DatabaseOperations as PostgreSQLDatabaseOperations,
)


class DatabaseOperations(PostgreSQLDatabaseOperations):
    """Opera de Django con identificadores esquema-calificados.

    El ``quote_name`` original envuelve el nombre completo
    (``"nucleo.usuario"``), que PostgreSQL lee como un identificador literal
    con punto en lugar de esquema + tabla.
    """

    def quote_name(self, name):
        if '"."' in name:
            # Ya partido por ``truncate_name()``: "nucleo"."usuario".
            parts = name.split('"."')
        elif "." in name and not (name.startswith('"') and name.endswith('"')):
            # Nombre crudo con esquema: nucleo.usuario -> "nucleo"."usuario".
            parts = name.split(".")
        else:
            return super().quote_name(name)
        return ".".join(
            '"%s"' % part.strip('"').replace('"', '""') for part in parts
        )
