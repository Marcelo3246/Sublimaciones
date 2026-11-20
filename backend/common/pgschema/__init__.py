"""Backend PostgreSQL con soporte de esquemas por módulo.

Django asume que ``Meta.db_table`` es un nombre plano que vive en el
``search_path``: lo cita como un único identificador (``"nucleo.usuario"``),
parte los identificadores solo por ``'"."'`` y deriva de ahí los nombres
auto-generados de índices y restricciones. Con la convención de esquemas de
``docs/06b-esquemas-y-ddl-postgresql.md`` (``nucleo.usuario``,
``ventas.pedido_venta``, ...) ese comportamiento crea las tablas en ``public``
con un punto en el nombre y rompe ``SET CONSTRAINTS`` al no encontrar la
restricción fuera del ``search_path``.

Este paquete extiende ``django.db.backends.postgresql``:

- :mod:`backend.common.pgschema.split`: parte ``esquema.tabla`` también sin
  comillas (nombres auto-generados y ``SET CONSTRAINTS`` de ``add_field``).
- :mod:`backend.common.pgschema.operations`: ``quote_name`` emite
  ``"esquema"."tabla"``.
- :mod:`backend.common.pgschema.introspection`: introspección calificada por
  esquema (el filtro ``pg_table_is_visible`` ocultaría las tablas).
- :mod:`backend.common.pgschema.schema`: renombrar/mover tablas entre
  esquemas y qualificar ``SET CONSTRAINTS`` al borrar una FK.
"""

from .split import patch_split_identifier, split_identifier

__all__ = ["patch_split_identifier", "split_identifier"]
