"""Partición de identificadores con esquema (``nucleo.usuario``)."""

from importlib import import_module

# Módulos de Django que importan ``split_identifier`` por valor y necesitan el
# parche: el editor de esquemas (nombres de índices/FK y SET CONSTRAINTS), el
# modelo de índices (nombres automáticos de ``Meta.indexes``) y el propio
# ``truncate_name``.
_TARGET_MODULES = (
    "django.db.backends.utils",
    "django.db.backends.base.schema",
    "django.db.models.indexes",
)


def split_identifier(identifier):
    """Como ``django.db.backends.utils.split_identifier``.

    Django solo parte por ``'"."'`` (punto entrecomillado), así que un
    identificador ``nucleo.usuario`` se toma como un nombre único: los nombres
    auto-generados de índices y restricciones incluirían el punto (rompería
    ``ADD CONSTRAINT``/``CREATE INDEX`` una vez que ``quote_name`` parte por
    esquema) y ``add_field`` no declararía el esquema en ``SET CONSTRAINTS``.

    Aquí también se parte por ``.`` sin comillas. Los identificadores sin
    punto se devuelven igual que Django (espacio de nombres vacío).
    """
    try:
        namespace, name = identifier.split('"."')
    except ValueError:
        namespace, _, name = identifier.rpartition(".")
    return namespace.strip('"'), name.strip('"')


def patch_split_identifier():
    """Instala :func:`split_identifier` en los módulos que lo importan.

    Idempotente. Se ejecuta desde ``backend/config/settings.py`` para que el
    parche esté activo antes de definir los modelos: ``Index`` sin nombre se
    autodenomina en el momento de crear la clase, antes de que exista
    conexión alguna a la base de datos.
    """
    for module_name in _TARGET_MODULES:
        module = import_module(module_name)
        if getattr(module, "split_identifier", None) is not split_identifier:
            module.split_identifier = split_identifier
