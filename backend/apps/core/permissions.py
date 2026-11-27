"""Permisos reutilizables para el núcleo del sistema."""

from rest_framework.permissions import SAFE_METHODS, BasePermission

from backend.apps.core.choices import RolUsuario


class SoloAdministrador(BasePermission):
    """Permite el acceso únicamente a usuarios administradores activos."""

    def has_permission(self, request, _view):  # pyright: ignore[reportIncompatibleMethodOverride]
        del _view
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.activo
            and user.rol == RolUsuario.ADMINISTRADOR
        )


class AccesoLocal(BasePermission):
    """Restringe la lectura de locales al alcance asignado al usuario."""

    def has_permission(self, request, _view):  # pyright: ignore[reportIncompatibleMethodOverride]
        del _view
        user = request.user
        if not user or not user.is_authenticated or not user.activo:
            return False

        return (
            request.method in SAFE_METHODS
            or user.rol == RolUsuario.ADMINISTRADOR
        )

    def has_object_permission(self, request, _view, obj):  # pyright: ignore[reportIncompatibleMethodOverride]
        del _view
        user = request.user
        if not user or not user.is_authenticated or not user.activo:
            return False

        if request.method not in SAFE_METHODS:
            return user.rol == RolUsuario.ADMINISTRADOR

        return (
            user.rol == RolUsuario.ADMINISTRADOR
            or user.es_global
            or user.local_id == obj.pk
        )