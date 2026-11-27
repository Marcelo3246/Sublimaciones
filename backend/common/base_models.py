"""Modelos base abstractos y mixins transversales para el monolito modular."""

from django.db import models


class TimeStampedModel(models.Model):
    """Mixin abstracto que agrega marcas de tiempo de creación y actualización."""

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActivoMixin(models.Model):
    """Mixin abstracto para borrado lógico."""

    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True
