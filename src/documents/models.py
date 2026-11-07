from django.conf import settings
from django.db import models
from core.common.models import Auditable


class PlantillaDocumento(Auditable):
    tipo_documento = models.CharField(max_length=50, help_text="factura, nota_entrega, orden_produccion, etc.")
    nombre = models.CharField(max_length=100)
    ruta_archivo = models.FileField(upload_to="plantillas/", blank=True, null=True)
    contenido = models.TextField(blank=True, default="", help_text="Plantilla HTML o contenido Jinja/Django")
    es_predeterminada = models.BooleanField(default=False)

    class Meta:
        db_table = "documents_plantilla_documento"
        verbose_name = "Plantilla de Documento"
        verbose_name_plural = "Plantillas de Documentos"

    def __str__(self):
        return f"{self.nombre} ({self.tipo_documento})"


class Documento(Auditable):
    class TipoDocumento(models.TextChoices):
        FACTURA = "factura", "Factura Propia"
        NOTA_ENTREGA = "nota_entrega", "Nota de Entrega"
        ORDEN_PRODUCCION = "orden_produccion", "Orden de Producción"
        PLANILLA_TRANSFERENCIA = "planilla_transferencia", "Planilla de Transferencia"
        ACTA_DESPERDICIO = "acta_desperdicio", "Acta de Desperdicio"
        COMPROBANTE_COMISION = "comprobante_comision", "Comprobante de Comisión"

    tipo_documento = models.CharField(max_length=50, choices=TipoDocumento.choices)
    local = models.ForeignKey("identity.Local", on_delete=models.PROTECT, related_name="documentos")
    numero_documento = models.CharField(max_length=50, unique=True)
    entidad_referencia = models.CharField(max_length=50, help_text="Nombre de la entidad generadora")
    id_referencia = models.IntegerField(help_text="ID del registro origen")
    plantilla = models.ForeignKey(PlantillaDocumento, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=20, default="emitido")
    ruta_archivo = models.FileField(upload_to="documentos_emitidos/", blank=True, null=True)
    generado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        db_table = "documents_documento"
        indexes = [
            models.Index(fields=["tipo_documento", "local", "creado_en"]),
        ]
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return f"{self.get_tipo_documento_display()} #{self.numero_documento} ({self.local.codigo})"
