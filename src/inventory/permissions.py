from rest_framework import permissions

class TieneAccesoAlLocal(permissions.BasePermission):
    """Verifica si el usuario en sesión tiene alcance sobre el local consultado."""
    def has_object_permission(self, request, view, obj):
        if getattr(request.user, "es_global", False):
            return True
        return getattr(obj, "local_id", None) == getattr(request.user, "local_predeterminado_id", None)
