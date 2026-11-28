"""Enumeraciones y choices para el módulo recursos humanos."""

from django.db import models


class CargoTrabajador(models.TextChoices):
    """Función que desempeña el trabajador dentro del negocio (RF-48)."""

    IMPRESOR = "IMPRESOR", "Impresor"
    VENDEDOR = "VENDEDOR", "Vendedor"
    DISENADOR = "DISENADOR", "Diseñador"
    PLANCHADOR = "PLANCHADOR", "Planchador"
    CONFECCIONADOR = "CONFECCIONADOR", "Confeccionador"
