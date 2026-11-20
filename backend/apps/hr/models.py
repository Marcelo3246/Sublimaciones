"""Modelos de datos para el módulo recursos humanos.

Implementa el catálogo de personal (Trabajador) y su asignación
multi-local (TrabajadorLocal) con class Meta y db_table explícito.

Fuente: especificación oficial RF-48 (docs/03-requerimientos-del-sistema.md),
docs/modelo-datos/06.9-rrhh.md y docs/ddl/06b.9-rrhh.md.
La nómina y las comisiones (RF-49 a RF-51) quedan diferidas a una fase
posterior (docs/09-decisiones-diferidas-y-fases.md).
"""

from django.db import models
from django.db.models import Q
from django.utils import timezone

from backend.apps.hr.choices import CargoTrabajador
from backend.common.base_models import ActivoMixin, TimeStampedModel


class Trabajador(TimeStampedModel, ActivoMixin):
    """Empleado del negocio (no confundir con el usuario del sistema)."""

    nombre_completo = models.CharField("nombre completo", max_length=150)
    cargo = models.CharField(
        "cargo",
        max_length=50,
        choices=CargoTrabajador.choices,
        help_text="Qué hace en el negocio; alimenta la asignación de producción",
    )
    telefono = models.CharField("teléfono", max_length=30, blank=True, default="")
    correo = models.EmailField("correo", max_length=150, blank=True, default="")
    fecha_ingreso = models.DateField("fecha de ingreso", default=timezone.localdate)
    # Referencia débil (sin FK en BD) al usuario del sistema, si tiene login.
    usuario = models.OneToOneField(
        "core.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_constraint=False,
        related_name="trabajador",
        verbose_name="usuario del sistema",
        help_text="Solo si el trabajador tiene acceso al sistema",
    )

    class Meta:
        verbose_name = "trabajador"
        verbose_name_plural = "trabajadores"
        db_table = "rrhh.trabajador"
        ordering = ["nombre_completo"]
        indexes = [
            models.Index(
                fields=["cargo"],
                condition=Q(activo=True),
                name="hr_trabajador_cargo_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(cargo__in=CargoTrabajador.values),
                name="hr_trabajador_cargo_ck",
            ),
        ]

    def __str__(self):
        return f"{self.nombre_completo} ({self.get_cargo_display()})"


class TrabajadorLocal(TimeStampedModel, ActivoMixin):
    """Asignación de un trabajador a un local; una sola sede principal."""

    trabajador = models.ForeignKey(
        Trabajador,
        on_delete=models.PROTECT,
        related_name="asignaciones",
        verbose_name="trabajador",
    )
    local = models.ForeignKey(
        "core.Local",
        on_delete=models.PROTECT,
        related_name="trabajadores_asignados",
        verbose_name="local",
    )
    es_principal = models.BooleanField("es local principal", default=False)

    class Meta:
        verbose_name = "asignación de trabajador a local"
        verbose_name_plural = "asignaciones de trabajadores a locales"
        db_table = "rrhh.trabajador_local"
        ordering = ["trabajador", "-es_principal", "local"]
        constraints = [
            models.UniqueConstraint(
                fields=["trabajador", "local"],
                name="hr_trabajador_local_uk",
            ),
            models.UniqueConstraint(
                fields=["trabajador"],
                condition=Q(es_principal=True),
                name="hr_trabajador_local_principal_uk",
            ),
        ]

    def __str__(self):
        principal = " (principal)" if self.es_principal else ""
        return f"{self.trabajador.nombre_completo} @ {self.local}{principal}"
