"""Configuración de Django para el proyecto DLL Sublimados."""

import os
from datetime import timedelta
from pathlib import Path

import dj_database_url

# BASE_DIR apunta a la raíz del repositorio
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Cargar variables de entorno desde .env en la raíz
env_file = BASE_DIR / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                v = v.strip()
                # Eliminar comillas envolventes simples o dobles (igual que python-decouple)
                if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
                    v = v[1:-1]
                os.environ.setdefault(k.strip(), v)

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-dll-sublimados-default-dev-key"
)

DEBUG = os.environ.get("DEBUG", "True").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if h.strip()
]
if "testserver" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("testserver")

# ============================================================
# Aplicaciones instaladas (Monolito Modular)
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
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
]

LOCAL_APPS = [
    "backend.apps.core",
    "backend.apps.catalog",
    "backend.apps.inventory",
    "backend.apps.purchasing",
    "backend.apps.production",
    "backend.apps.sales",
    "backend.apps.pricing",
    "backend.apps.hr",
    "backend.apps.documents",
    "backend.apps.reports",
    "backend.apps.audit",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Modelo de usuario personalizado obligatorio desde el inicio
AUTH_USER_MODEL = "core.Usuario"

# ============================================================
# Middleware
# ============================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "backend.config.wsgi.application"
ASGI_APPLICATION = "backend.config.asgi.application"

# ============================================================
# Base de datos (PostgreSQL 14+ / Neon)
# ============================================================
# Django no admite Meta.db_table con esquema ("nucleo.usuario"): lo cita como
# un único identificador y deriva de él los nombres auto-generados de índices
# y restricciones. El backend propio backend.common.pgschema corrige eso más
# la introspección y el renombrado de tablas. El parche de identificadores se
# aplica aquí para que esté activo antes de cargar los modelos (los índices
# sin nombre se autodenominan al definir la clase).
from backend.common.pgschema import patch_split_identifier  # noqa: E402

patch_split_identifier()

# Prioridad 1: DATABASE_URL (Neon — pooler PgBouncer).
# Prioridad 2: DB_ENGINE=sqlite3 (pruebas rápidas locales).
# Prioridad 3: Variables sueltas DB_* (PostgreSQL local sin Neon).
#
# IMPORTANTE: para migraciones usar DATABASE_URL_UNPOOLED (endpoint directo):
#   DATABASE_URL=$DATABASE_URL_UNPOOLED python manage.py migrate
_database_url = os.environ.get("DATABASE_URL")

if _database_url:
    DATABASES = {
        "default": dj_database_url.config(
            default=_database_url,
            conn_max_age=600,         # keep-alive: reutiliza conexiones al pooler
            conn_health_checks=True,  # descarta conexiones zombi automáticamente
            ssl_require=True,         # Neon exige SSL
        )
    }
elif "sqlite3" in os.environ.get("DB_ENGINE", "postgresql"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # Desarrollo local sin Neon
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
            "NAME": os.environ.get("DB_NAME", "dll_sublimados"),
            "USER": os.environ.get("DB_USER", "postgres"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }

# Sustituir el motor de Django por el backend propio cuando se usa PostgreSQL
# (añade esquemas por módulo; SQLite no se toca).
if DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":
    DATABASES["default"]["ENGINE"] = "backend.common.pgschema"

# ============================================================
# Password validation
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]

# ============================================================
# Internacionalización
# ============================================================
LANGUAGE_CODE = "es-ve"
TIME_ZONE = "America/Caracas"
USE_I18N = True
USE_TZ = True

# ============================================================
# Archivos estáticos y multimedia
# ============================================================
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================================
# Django REST Framework & SimpleJWT
# ============================================================

AUTH_USER_MODEL = "core.Usuario"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),
    "PAGE_SIZE": 20,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes = 15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ============================================================
# CORS (Frontend SPA React)
# ============================================================
cors_origins = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
)
CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in cors_origins.split(",") if origin.strip()
]
CORS_ALLOW_CREDENTIALS = True
