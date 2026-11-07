from django.conf import settings
from django.db import models


# ---------------------------------------------------------------------------
# Modelo abstracto: Auditable
# ---------------------------------------------------------------------------

class Auditable(models.Model):
    """Modelo abstracto que agrega campos de auditoría a cualquier entidad.

    Campos incluidos:
    - creado_en / actualizado_en: timestamps automáticos.
    - creado_por: referencia al usuario que creó el registro (nullable para
      procesos del sistema o migraciones).
    - activo: borrado lógico; False = registro "eliminado" sin perder data.
    """

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_creados",
    )
    activo = models.BooleanField(
        default=True,
        help_text="False = registro desactivado (borrado lógico).",
    )

    class Meta:
        abstract = True


# ---------------------------------------------------------------------------
# Modelo abstracto: MontoMonetario
# ---------------------------------------------------------------------------

class MontoMonetario(models.Model):
    """Modelo abstracto para campos monetarios con monto y moneda.

    TODO (pendiente por implementar):
    - Validación de monto positivo según contexto de negocio.
    - Helper para conversión automática USD ↔ BS usando TasaCambio.
    """

    class Moneda(models.TextChoices):
        USD = "USD", "Dólares (USD)"
        BS = "BS", "Bolívares (BS)"

    monto = models.DecimalField(max_digits=14, decimal_places=2)
    moneda = models.CharField(
        max_length=3,
        choices=Moneda.choices,
        default=Moneda.USD,
    )

    class Meta:
        abstract = True


# ---------------------------------------------------------------------------
# Modelo concreto: TasaCambio
# ---------------------------------------------------------------------------

class TasaCambio(Auditable):
    """Registro diario de la tasa de cambio USD → BS.

    Cada día debe tener una única tasa vigente.  Se utiliza en todos los
    módulos que manejan montos monetarios para la conversión entre monedas.

    TODO (pendiente por implementar):
    - Método/property para conversión inversa (BS → USD).
    - Signal o servicio que valide que no existan duplicados de fecha.
    """

    fecha_vigencia = models.DateField(unique=True)
    dolares_a_bs = models.DecimalField(max_digits=12, decimal_places=4)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="tasas_cambio_registradas",
    )

    class Meta:
        db_table = "common_tasa_cambio"
        ordering = ["-fecha_vigencia"]
        verbose_name = "Tasa de Cambio"
        verbose_name_plural = "Tasas de Cambio"

    def __str__(self):
        return f"{self.fecha_vigencia} — 1 USD = {self.dolares_a_bs} BS"
