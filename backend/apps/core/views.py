"""Vistas de API para el módulo núcleo."""

from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.apps.core.models import Local, Usuario
from backend.apps.core.serializers import LocalSerializer, UsuarioSerializer


class LocalViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.filter(activo=True)
    serializer_class = LocalSerializer
    permission_classes = [permissions.IsAuthenticated]


class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Usuario.objects.filter(activo=True)
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]


class PerfilUsuarioView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)
