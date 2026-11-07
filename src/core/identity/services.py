"""
core.identity.services
======================

Capa de servicios (lógica de negocio) del módulo Identity.

Pendiente por implementar:
--------------------------

crear_usuario(data, creado_por=None)
    Crea un Usuario, le asigna locales y roles, y registra la acción
    en la bitácora de auditoría.

asignar_rol(usuario, rol, local=None)
    Asigna un Rol a un Usuario en un Local (o globalmente si local=None).
    Valida que no exista duplicado.

revocar_rol(usuario, rol, local=None)
    Elimina la asignación de rol.

usuario_tiene_permiso(usuario, codigo_permiso, local=None) -> bool
    Recorre UsuarioRol → RolPermiso para determinar si el usuario posee
    el permiso indicado en el local dado.  Si el usuario es ``es_global``
    o tiene el rol asignado sin local, aplica globalmente.

obtener_locales_del_usuario(usuario) -> QuerySet[Local]
    Retorna los locales a los que tiene acceso un usuario (vía UsuarioLocal),
    o todos si ``es_global=True``.
"""
