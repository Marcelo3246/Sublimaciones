"""
Configuración de Django para el proyecto DLL Sublimados.

Sistema de gestión integral para un negocio de sublimación, planchado
y confección distribuido en 3 locales, con servidor central único.

Arquitectura: Monolito modular Django + PostgreSQL
Frontend: React + Vite + Tailwind CSS (SPA que consume esta API REST)
Documentación: /docs/04 Arquitectura del monolito modular.md
"""

import os
from datetime import timedelta
from pathlib import Path

from decouple import Csv, config

# ============================================================
# Rutas base
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# Seguridad
# ============================================================
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost", cast=Csv())

# ============================================================
# Aplicaciones instaladas
# ============================================================
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
]

# ── Apps propias del proyecto (monolito modular) ─────────────
# Orden: core primero, luego módulos de negocio según dependencias.
# Ref: docs/04 Arquitectura del monolito modular.md
LOCAL_APPS = [
    # --- Core (sin dependencias de negocio) ---
    "core.common",       # Abstracts: Auditable, MontoMonetario, secuencias, TasaCambio
    "core.identity",     # Login, usuarios, roles, permisos, locales
    "core.audit",        # Bitácora de acciones y de stock

    # --- Módulos de negocio (proveedores de datos) ---
    "catalog",           # Materias primas, productos, servicios, categorías, UM, tallas, diseños
    "pricing",           # Matriz de precios, fórmula, historial, tasa de cambio

    # --- Módulos de negocio (consumidores) ---
    "inventory",         # Stock por local, partidas, movimientos, transferencias
    "purchasing",        # Proveedores, órdenes de compra, facturas, comparador de precios
    "production",        # Órdenes de producción, ruta multi-local, consumo, máquinas
    "sales",             # Clientes, pedidos, facturación propia, multi-moneda
    "hr",                # Trabajadores, comisiones, pagos, adelantos

    # --- Módulos transversales (solo leen) ---
    "documents",         # Generador de documentos: facturas, notas, planillas
    "reports",           # Dashboard y reportes por local / KPIs
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ============================================================
# Middleware
# ============================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS antes de CommonMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ============================================================
# Templates
# ============================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ============================================================
# Base de datos — PostgreSQL 14+ en servidor central (RNF-02)
# Permite SQLite como alternativa para desarrollo/pruebas locales si se define en .env
# ============================================================
DB_ENGINE = config("DB_ENGINE", default="django.db.backends.postgresql")

if "sqlite" in DB_ENGINE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / config("DB_NAME", default="db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": DB_ENGINE,
            "NAME": config("DB_NAME", default="dll_sublimados"),
            "USER": config("DB_USER", default="postgres"),
            "PASSWORD": config("DB_PASSWORD", default="postgres"),
            "HOST": config("DB_HOST", default="localhost"),
            "PORT": config("DB_PORT", default="5432"),
            "OPTIONS": {
                "options": "-c search_path=public",
            },
            "ATOMIC_REQUESTS": True,  # RNF-04: toda vista en transacción
        }
    }

# ============================================================
# Modelo de usuario personalizado (core.identity)
# ============================================================
AUTH_USER_MODEL = "identity.Usuario"

# ============================================================
# Validación de contraseñas (RNF-03)
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ============================================================
# Internacionalización (RNF-08: español neutro en UI)
# ============================================================
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Caracas"
USE_I18N = True
USE_TZ = True

# ============================================================
# Archivos estáticos y media
# ============================================================
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Subdirectorios de media para archivos del negocio
# media/disenos/    → archivos de diseño (RF-12)
# media/documentos/ → PDFs emitidos (RF-52)
# media/facturas/   → imágenes/PDF de facturas de compra (RF-27)

# ============================================================
# Clave primaria por defecto
# ============================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================================
# Django REST Framework
# ============================================================
REST_FRAMEWORK = {
    # Autenticación JWT (RNF-03)
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # Permisos: por defecto requiere autenticación
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    # Paginación
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
    # Filtros
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    # Renderers
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    # Formato de fechas
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
    "DATE_FORMAT": "%Y-%m-%d",
}

# ============================================================
# Simple JWT — tokens de autenticación
# ============================================================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    # Claims personalizados para el alcance por local
    "TOKEN_OBTAIN_SERIALIZER": "core.identity.serializers.CustomTokenObtainPairSerializer",
}

# ============================================================
# CORS — permite la SPA React en desarrollo y producción
# ============================================================
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:5173",
    cast=Csv(),
)
CORS_ALLOW_CREDENTIALS = True

# ============================================================
# Configuración del negocio — DLL Sublimados
# ============================================================

# Fórmula de precio (RF-45): precio_base × MARGEN × IVA
# Parametrizable si las tasas cambian
PRECIO_MARGEN_DEFAULT = 1.30   # 30% de margen
PRECIO_IVA_DEFAULT = 1.16      # 16% de IVA

# Monedas soportadas (RNF-05)
MONEDAS = [
    ("USD", "Dólar estadounidense"),
    ("BS", "Bolívar"),
]
MONEDA_REFERENCIA = "USD"

# Tipo de cambio por defecto (editable por admin en TasaCambio)
TASA_CAMBIO_DEFAULT = config("TASA_CAMBIO_DEFAULT", default="36.50", cast=float)
