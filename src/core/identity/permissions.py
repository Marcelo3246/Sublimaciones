"""
core.identity.permissions
=========================

Clases de permisos personalizadas para DRF y utilidades de autorización.

Pendiente por implementar:
--------------------------

TienePermiso(BasePermission)
    Permiso DRF que verifica si el usuario autenticado posee un permiso
    de negocio específico (código del tipo ``modulo.entidad.accion``)
    opcionalmente dentro de un Local dado.  Consulta la cadena:
    UsuarioRol → RolPermiso → Permiso.

EsAdministradorGlobal(BasePermission)
    Permiso que solo permite acceso a usuarios con ``es_global=True``.

EsDelLocal(BasePermission)
    Verifica que el usuario pertenezca al Local indicado en la URL
    (vía UsuarioLocal o ``es_global``).
"""
