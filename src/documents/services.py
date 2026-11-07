"""Servicios transversales para emisión de documentos."""
from .models import Documento


def generate_document(doc_type: str, ref_obj, user_id=None):
    """Genera un documento (factura, nota de entrega, etc.) en PDF y registra su número correlativo (RF-52)."""
    # TODO: Implementar renderizador PDF y correlativos por (tipo, local, año)
    pass


def obtener_siguiente_numero(tipo_documento: str, local_id: int) -> str:
    """Calcula el siguiente correlativo atómico con bloqueo FOR UPDATE (RF-54)."""
    # TODO: Implementar generador de secuencia correlativa
    return "0001"
