"""Pruebas del módulo núcleo e identidad."""

from decimal import Decimal
from typing import cast

from django.test import TestCase
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.test import APIClient

from backend.apps.core.choices import TipoComprobante
from backend.apps.core.models import (
    ContadorCorrelativo,
    Local,
    TasaCambio,
    Usuario,
    UsuarioManager,
)


class CoreModelsTest(TestCase):
    def setUp(self):
        self.local = Local.objects.create(
            codigo="L01",
            nombre="Local Principal",
            persona_contacto="Admin Central",
        )
        manager = cast(UsuarioManager, Usuario.objects)
        self.user = manager.create_user(
            nombre_usuario="testuser",
            correo="test@example.com",
            password="securepassword",
        )

    def test_crear_local(self):
        self.assertEqual(str(self.local), "L01 - Local Principal")
        self.assertEqual(self.local.persona_contacto, "Admin Central")

    def test_crear_usuario(self):
        self.assertTrue(self.user.check_password("securepassword"))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_login_entrega_tokens_con_credenciales_validas(self):
        response = APIClient().post(
            "/api/v1/auth/token/",
            {
                "nombre_usuario": self.user.nombre_usuario,
                "password": "securepassword",
            },
            format="json",
        )
        assert isinstance(response, Response)

        self.assertEqual(response.status_code, 200)
        assert response.data is not None
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_rechaza_contrasena_incorrecta(self):
        response = APIClient().post(
            "/api/v1/auth/token/",
            {
                "nombre_usuario": self.user.nombre_usuario,
                "password": "incorrecta",
            },
            format="json",
        )
        assert isinstance(response, Response)

        self.assertEqual(response.status_code, 401)

    def test_refresh_rota_token_y_rechaza_el_token_anterior(self):
        client = APIClient()
        login = client.post(
            "/api/v1/auth/token/",
            {
                "nombre_usuario": self.user.nombre_usuario,
                "password": "securepassword",
            },
            format="json",
        )
        old_refresh = login.data["refresh"]

        response = client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": old_refresh},
            format="json",
        )
        assert isinstance(response, Response)

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertNotEqual(response.data["refresh"], old_refresh)

        replay_response = client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": old_refresh},
            format="json",
        )
        self.assertEqual(replay_response.status_code, 401)

    def test_logout_revoca_refresh_token(self):
        client = APIClient()
        login = client.post(
            "/api/v1/auth/token/",
            {
                "nombre_usuario": self.user.nombre_usuario,
                "password": "securepassword",
            },
            format="json",
        )
        refresh = login.data["refresh"]

        logout = client.post(
            "/api/v1/auth/token/logout/",
            {"refresh": refresh},
            format="json",
        )
        self.assertEqual(logout.status_code, 200)

        refresh_response = client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": refresh},
            format="json",
        )
        self.assertEqual(refresh_response.status_code, 401)

    def test_perfil_requiere_token_y_devuelve_usuario_autenticado(self):
        client = APIClient()
        anonymous_response = client.get("/api/v1/core/perfil/")
        self.assertEqual(anonymous_response.status_code, 401)

        login = client.post(
            "/api/v1/auth/token/",
            {
                "nombre_usuario": self.user.nombre_usuario,
                "password": "securepassword",
            },
            format="json",
        )
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        profile_response = client.get("/api/v1/core/perfil/")
        assert isinstance(profile_response, Response)

        self.assertEqual(profile_response.status_code, 200)
        self.assertEqual(
            profile_response.data["nombre_usuario"], self.user.nombre_usuario
        )

    def test_usuario_sin_local_no_ve_locales(self):
        client = APIClient()
        login = client.post(
            "/api/v1/auth/token/",
            {
                "nombre_usuario": self.user.nombre_usuario,
                "password": "securepassword",
            },
            format="json",
        )
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")

        response = client.get("/api/v1/core/locales/")
        assert isinstance(response, Response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)

    def test_usuario_ve_solo_su_local_y_usuario_global_ve_todos(self):
        otro_local = Local.objects.create(
            codigo="L02",
            nombre="Local Secundario",
        )
        self.user.local = self.local
        self.user.save(update_fields=["local"])

        client = APIClient()
        login = client.post(
            "/api/v1/auth/token/",
            {
                "nombre_usuario": self.user.nombre_usuario,
                "password": "securepassword",
            },
            format="json",
        )
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        local_response = client.get("/api/v1/core/locales/")
        self.assertEqual(local_response.data["count"], 1)
        self.assertEqual(local_response.data["results"][0]["id"], self.local.pk)

        self.user.es_global = True
        self.user.save(update_fields=["es_global"])
        global_login = client.post(
            "/api/v1/auth/token/",
            {
                "nombre_usuario": self.user.nombre_usuario,
                "password": "securepassword",
            },
            format="json",
        )
        client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {global_login.data['access']}"
        )
        global_response = client.get("/api/v1/core/locales/")
        self.assertEqual(global_response.data["count"], 2)
        self.assertIn(
            otro_local.pk,
            [local["id"] for local in global_response.data["results"]],
        )

    def test_listado_usuarios_requiere_rol_administrador(self):
        client = APIClient()
        login = client.post(
            "/api/v1/auth/token/",
            {
                "nombre_usuario": self.user.nombre_usuario,
                "password": "securepassword",
            },
            format="json",
        )
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        self.assertEqual(client.get("/api/v1/core/usuarios/").status_code, 403)

        admin = Usuario.objects.create_superuser(
            nombre_usuario="admin",
            correo="admin@example.com",
            password="adminpassword",
        )
        admin_login = client.post(
            "/api/v1/auth/token/",
            {
                "nombre_usuario": admin.nombre_usuario,
                "password": "adminpassword",
            },
            format="json",
        )
        client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {admin_login.data['access']}"
        )
        self.assertEqual(client.get("/api/v1/core/usuarios/").status_code, 200)

    def test_tasa_cambio_y_obtener_vigente(self):
        tasa = TasaCambio.objects.create(
            fecha_vigencia=timezone.now().date(),
            dolares_a_bs=Decimal("36.5000"),
            registrado_por=self.user,
        )
        self.assertIn("36.5000", str(tasa))
        vigente = TasaCambio.obtener_vigente()
        self.assertIsNotNone(vigente)
        assert vigente is not None
        self.assertEqual(vigente.dolares_a_bs, Decimal("36.5000"))

    def test_contador_correlativo_obtener_siguiente(self):
        correlativo_1 = ContadorCorrelativo.obtener_siguiente(
            tipo_comprobante=TipoComprobante.FACTURA,
            local=self.local,
            anio=2026,
            prefijo="FAC",
        )
        self.assertEqual(correlativo_1, "FAC-2026-000001")

        correlativo_2 = ContadorCorrelativo.obtener_siguiente(
            tipo_comprobante=TipoComprobante.FACTURA,
            local=self.local,
            anio=2026,
            prefijo="FAC",
        )
        self.assertEqual(correlativo_2, "FAC-2026-000002")

        contador = ContadorCorrelativo.objects.get(
            tipo_comprobante=TipoComprobante.FACTURA,
            local=self.local,
            anio=2026,
        )
        self.assertEqual(contador.numero_actual, 2)
