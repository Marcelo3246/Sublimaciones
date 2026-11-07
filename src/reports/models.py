"""Módulo de Reportes.

Nota de Arquitectura:
Este módulo NO define tablas propias de negocio en la base de datos (RF-56, RF-57).
Su responsabilidad es agregar, calcular indicadores y generar vistas/reportes
a partir de las tablas de los otros módulos (sales, inventory, production, purchasing, hr).
"""
from django.db import models
