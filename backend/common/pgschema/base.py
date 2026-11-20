"""Backend PostgreSQL con soporte de esquemas por módulo."""

from django.db.backends.postgresql.base import (
    DatabaseWrapper as PostgreSQLDatabaseWrapper,
)

from .introspection import DatabaseIntrospection
from .operations import DatabaseOperations
from .schema import DatabaseSchemaEditor


class DatabaseWrapper(PostgreSQLDatabaseWrapper):
    """Conexión PostgreSQL que sustituye esquema, introspección y operaciones.

    Se activa con ``ENGINE = "backend.common.pgschema"`` en
    ``backend/config/settings.py``. El resto del comportamiento (psycopg,
    pooler, SSL, transacciones) es el de Django.
    """

    SchemaEditorClass = DatabaseSchemaEditor
    introspection_class = DatabaseIntrospection
    ops_class = DatabaseOperations
