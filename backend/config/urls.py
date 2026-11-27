"""Configuración de URLs del backend de DLL Sublimados."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # JWT Authentication
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Core API
    path("api/v1/core/", include("backend.apps.core.urls")),
    # Apps de negocio
    path("api/v1/catalog/", include("backend.apps.catalog.urls")),
    path("api/v1/inventory/", include("backend.apps.inventory.urls")),
    path("api/v1/purchasing/", include("backend.apps.purchasing.urls")),
    path("api/v1/production/", include("backend.apps.production.urls")),
    path("api/v1/sales/", include("backend.apps.sales.urls")),
    path("api/v1/pricing/", include("backend.apps.pricing.urls")),
    path("api/v1/hr/", include("backend.apps.hr.urls")),
    path("api/v1/documents/", include("backend.apps.documents.urls")),
    path("api/v1/reports/", include("backend.apps.reports.urls")),
    path("api/v1/audit/", include("backend.apps.audit.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
