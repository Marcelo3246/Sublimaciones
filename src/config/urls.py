"""
URL Configuration del proyecto DLL Sublimados.

Punto de entrada para todas las rutas de la API REST.
Cada módulo registra sus propias rutas en su archivo urls.py.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Admin de Django
    path("admin/", admin.site.urls),

    # ── API v1 ───────────────────────────────────────────────
    # Core
    path("api/v1/identity/", include("core.identity.urls")),
    path("api/v1/audit/", include("core.audit.urls")),

    # Módulos de negocio
    path("api/v1/catalog/", include("catalog.urls")),
    path("api/v1/inventory/", include("inventory.urls")),
    path("api/v1/purchasing/", include("purchasing.urls")),
    path("api/v1/production/", include("production.urls")),
    path("api/v1/sales/", include("sales.urls")),
    path("api/v1/pricing/", include("pricing.urls")),
    path("api/v1/hr/", include("hr.urls")),
    path("api/v1/documents/", include("documents.urls")),
    path("api/v1/reports/", include("reports.urls")),
]
