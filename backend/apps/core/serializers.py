"""Serializers de DRF para el núcleo del sistema."""

from rest_framework import serializers

from backend.apps.core.models import Local, Usuario


class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = ["id", "codigo", "nombre", "direccion", "telefono", "activo"]


class UsuarioSerializer(serializers.ModelSerializer):
    local_info = LocalSerializer(source="local", read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "nombre_usuario",
            "correo",
            "nombre",
            "apellido",
            "rol",
            "local",
            "local_info",
            "es_global",
            "activo",
        ]
        read_only_fields = ["id"]
