"""Modelos de datos para el módulo documentos.

Implementa el generador transversal de documentos: plantillas editables
y repositorio de comprobantes emitidos.
"""

from django.db import models
from django.utils import timezone

from backend.apps.documents.choices import EstadoDocumento, TipoDocumento
from backend.common.base_models import ActivoMixin, TimeStampedModel


def get_current_year():
    return timezone.now().year


class PlantillaDocumento(TimeStampedModel, ActivoMixin):
    """Plantilla editable para emisión de documentos con variables dinámicas."""

    codigo = models.CharField("código", max_length=50, unique=True)
    nombre = models.CharField("nombre", max_length=150)
    tipo = models.CharField(
        "tipo de documento", max_length=50, choices=TipoDocumento.choices
    )
    contenido_html = models.TextField(
        "contenido HTML",
        help_text="Plantilla HTML con variables dinámicas Jinja/Django",
    )
    version = models.CharField("versión", max_length=20, default="1.0")
    es_predeterminada = models.BooleanField("es predeterminada", default=False)
    ruta_archivo = models.CharField(
        "ruta de archivo base o membrete", max_length=500, blank=True, default=""
    )

    class Meta:
        verbose_name = "plantilla de documento"
        verbose_name_plural = "plantillas de documentos"
        db_table = "documentos.plantilla_documento"
        ordering = ["tipo", "nombre"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre} (v{self.version})"


class Documento(TimeStampedModel):
    """Registro inmutable de documento generado y emitido en el repositorio."""

    correlativo = models.CharField("correlativo", max_length=50)
    tipo_documento = models.CharField(
        "tipo de documento", max_length=50, choices=TipoDocumento.choices
    )
    local = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        related_name="documentos_emitidos",
        verbose_name="local",
    )
    anio = models.PositiveSmallIntegerField("año", default=get_current_year)
    plantilla = models.ForeignKey(
        PlantillaDocumento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documentos",
        verbose_name="plantilla",
    )
    entidad_tipo = models.CharField(
        "tipo de entidad origen", max_length=50, blank=True, default=""
    )
    entidad_id = models.BigIntegerField(
        "ID de entidad origen", null=True, blank=True
    )
    generado_por = models.ForeignKey(
        "core.Usuario",
        on_delete=models.PROTECT,
        related_name="documentos_generados",
        verbose_name="generado por",
    )
    fecha_emision = models.DateTimeField(
        "fecha de emisión", default=timezone.now
    )
    hash_seguridad = models.CharField(
        "hash de seguridad (SHA-256)", max_length=64, blank=True, default=""
    )
    url_archivo = models.CharField(
        "URL o ruta de archivo PDF", max_length=500, blank=True, default=""
    )
    estado = models.CharField(
        "estado",
        max_length=20,
        choices=EstadoDocumento.choices,
        default=EstadoDocumento.GENERADO,
    )

    class Meta:
        verbose_name = "documento"
        verbose_name_plural = "documentos"
        db_table = "documentos.documento"
        ordering = ["-fecha_emision"]
        constraints = [
            models.UniqueConstraint(
                fields=["tipo_documento", "local", "anio", "correlativo"],
                name="documents_documento_correlativo_uk",
            )
        ]
        indexes = [
            models.Index(
                fields=["tipo_documento", "local", "correlativo"],
                name="documents_doc_repo_idx",
            ),
            models.Index(
                fields=["entidad_tipo", "entidad_id"],
                name="documents_doc_entidad_idx",
            ),
        ]

    def __str__(self):
        return f"{self.tipo_documento} {self.correlativo} ({self.local.codigo})"
