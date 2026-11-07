"""
core.identity.serializers
=========================

Serializadores DRF y configuración de tokens JWT para el sistema
DLL Sublimados.
"""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer personalizado que agrega claims de negocio al token JWT.

    Claims adicionales incluidos en el token:
    - ``es_global``: indica si el usuario tiene acceso global.
    - ``local_predeterminado_id``: PK del local por defecto del usuario.

    TODO (pendiente por implementar):
    - Agregar claim con la lista de roles del usuario.
    - Agregar claim con la lista de locales autorizados.
    - Vista ``CustomTokenObtainPairView`` que use este serializer.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Claims personalizados
        token["es_global"] = user.es_global
        token["local_predeterminado_id"] = (
            user.local_predeterminado_id if user.local_predeterminado_id else None
        )

        return token
