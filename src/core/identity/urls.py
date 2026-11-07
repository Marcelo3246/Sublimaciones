"""
core.identity.urls
==================

Rutas del módulo Identity — Usuarios, Autenticación y Locales.

Rutas futuras planificadas:
---------------------------

Auth / JWT:
    POST   /auth/login/           → Obtener par de tokens (access + refresh)
    POST   /auth/refresh/         → Refrescar token de acceso
    POST   /auth/logout/          → Invalidar refresh token (blacklist)

Perfil:
    GET    /perfil/               → Datos del usuario autenticado
    PATCH  /perfil/               → Actualizar perfil propio

Locales (CRUD):
    GET    /locales/              → Listar locales
    POST   /locales/              → Crear local
    GET    /locales/{id}/         → Detalle de un local
    PATCH  /locales/{id}/         → Actualizar local
    DELETE /locales/{id}/         → Desactivar local (borrado lógico)

Usuarios (CRUD):
    GET    /usuarios/             → Listar usuarios
    POST   /usuarios/             → Crear usuario
    GET    /usuarios/{id}/        → Detalle de un usuario
    PATCH  /usuarios/{id}/        → Actualizar usuario
    DELETE /usuarios/{id}/        → Desactivar usuario (borrado lógico)

Roles y Permisos:
    GET    /roles/                → Listar roles con sus permisos
    POST   /usuarios/{id}/roles/  → Asignar rol a usuario
    DELETE /usuarios/{id}/roles/  → Revocar rol de usuario
"""

from django.urls import path

app_name = "identity"

urlpatterns = [
    # TODO: Agregar rutas aquí conforme se implementen las vistas.
]
