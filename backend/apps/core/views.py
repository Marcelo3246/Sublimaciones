"""Vistas de API para el módulo núcleo."""

from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.apps.core.choices import RolUsuario
from backend.apps.core.models import Local, Usuario
from backend.apps.core.serializers import LocalSerializer, UsuarioSerializer
from backend.apps.core.permissions import AccesoLocal, SoloAdministrador


class LocalViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.filter(activo=True)
    serializer_class = LocalSerializer
    permission_classes = [AccesoLocal]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.rol == RolUsuario.ADMINISTRADOR or user.es_global:
            return queryset

        if user.local_id is None:
            return queryset.none()

        return queryset.filter(pk=user.local_id)


class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Usuario.objects.filter(activo=True)
    serializer_class = UsuarioSerializer
    permission_classes = [SoloAdministrador]


class PerfilUsuarioView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)