"""Configuración ASGI para el backend de DLL Sublimados."""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings")

application = get_asgi_application()
