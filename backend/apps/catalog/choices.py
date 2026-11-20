"""Enumeraciones y choices para el módulo catálogo."""

from django.db import models


class TipoCategoria(models.TextChoices):
    """Dominio al que pertenece una categoría del catálogo."""

    MATERIAL = "MATERIAL", "Material"
    PRODUCTO = "PRODUCTO", "Producto"
    SERVICIO = "SERVICIO", "Servicio"


class TipoProducto(models.TextChoices):
    """Clasificación comercial de un producto del catálogo."""

    TERMINADO = "TERMINADO", "Producto terminado"
    SEMITERMINADO = "SEMITERMINADO", "Producto semiterminado"
    SERVICIO = "SERVICIO", "Servicio"
