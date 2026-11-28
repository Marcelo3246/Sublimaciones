"""URLs de la API para el módulo núcleo."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from backend.apps.core.views import LocalViewSet, PerfilUsuarioView, UsuarioViewSet

router = DefaultRouter()
router.register(r"locales", LocalViewSet, basename="local")
router.register(r"usuarios", UsuarioViewSet, basename="usuario")

urlpatterns = [
    path("", include(router.urls)),
    path("perfil/", PerfilUsuarioView.as_view(), name="perfil-usuario"),
]
