"""Modelos de datos del núcleo e identidad del sistema.

Implementa la clase Meta con db_table explícito para cumplir con el
estándar de arquitectura del monolito modular.
"""

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models, transaction
from django.utils import timezone

from backend.apps.core.choices import RolUsuario, TipoComprobante
from backend.common.base_models import ActivoMixin, TimeStampedModel


class Local(TimeStampedModel, ActivoMixin):
    """Representa cada una de las sucursales o locales del negocio."""

    codigo = models.CharField("código", max_length=10, unique=True)
    nombre = models.CharField("nombre", max_length=100)
    direccion = models.CharField("dirección", max_length=255, blank=True, default="")
    telefono = models.CharField("teléfono", max_length=50, blank=True, default="")
    persona_contacto = models.CharField(
        "persona de contacto", max_length=100, blank=True, default=""
    )

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        verbose_name = "local"
        verbose_name_plural = "locales"
        db_table = "nucleo.local"

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class UsuarioManager(BaseUserManager):
    """Manager personalizado para el modelo Usuario."""

    def create_user(self, nombre_usuario, correo, password=None, **extra_fields):
        if not nombre_usuario:
            raise ValueError("El nombre de usuario es obligatorio")
        if not correo:
            raise ValueError("El correo electrónico es obligatorio")
        correo = self.normalize_email(correo)
        extra_fields.setdefault("activo", True)
        usuario = self.model(
            nombre_usuario=nombre_usuario, correo=correo, **extra_fields
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, nombre_usuario, correo, password=None, **extra_fields):
        extra_fields.setdefault("rol", RolUsuario.ADMINISTRADOR)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("es_global", True)
        extra_fields.setdefault("activo", True)
        return self.create_user(nombre_usuario, correo, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin, TimeStampedModel, ActivoMixin):
    """Modelo de usuario centralizado para autenticación y control de acceso."""

    nombre_usuario = models.CharField(
        "nombre de usuario", max_length=150, unique=True
    )
    correo = models.EmailField("correo electrónico", max_length=254, unique=True)
    nombre = models.CharField("nombre", max_length=150, blank=True, default="")
    apellido = models.CharField("apellido", max_length=150, blank=True, default="")
    rol = models.CharField(
        "rol",
        max_length=20,
        choices=RolUsuario.choices,
        default=RolUsuario.VENDEDOR,
    )
    local = models.ForeignKey(
        Local,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="usuarios",
        verbose_name="local",
    )
    es_global = models.BooleanField("alcance global", default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = "nombre_usuario"
    REQUIRED_FIELDS = ["correo"]

    @property
    def is_active(self):  # pyright: ignore[reportIncompatibleVariableOverride]
        return self.activo

    @property
    def is_staff(self):
        return self.is_superuser or self.rol == RolUsuario.ADMINISTRADOR

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        db_table = "nucleo.usuario"

    def __str__(self):
        return f"{self.nombre_usuario} ({self.get_rol_display()})"

    def get_rol_display(self):
        """Retorna la etiqueta legible del rol del usuario."""
        for valor, etiqueta in RolUsuario.choices:
            if str(valor) == str(self.rol):
                return str(etiqueta)
        return str(self.rol)


class TasaCambio(TimeStampedModel, ActivoMixin):
    """Serie temporal del tipo de cambio oficial (USD a Bs)."""

    fecha_vigencia = models.DateField(
        "fecha de vigencia", default=timezone.now
    )
    dolares_a_bs = models.DecimalField(
        "tasa USD a Bs", max_digits=14, decimal_places=4
    )
    registrado_por = models.ForeignKey(
        "core.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasas_cambio_registradas",
        verbose_name="registrado por",
    )

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        verbose_name = "tasa de cambio"
        verbose_name_plural = "tasas de cambio"
        db_table = "nucleo.tasa_cambio"
        ordering = ["-fecha_vigencia", "-creado_en"]
        indexes = [
            models.Index(
                fields=["-fecha_vigencia", "-creado_en"],
                name="core_tasa_vigencia_idx",
            ),
        ]

    def __str__(self):
        return f"{self.fecha_vigencia}: {self.dolares_a_bs} Bs/USD"

    @classmethod
    def obtener_vigente(cls):
        """Retorna la última tasa de cambio activa registrada."""
        return cls.objects.filter(activo=True).order_by("-fecha_vigencia", "-creado_en").first()


class ContadorCorrelativo(TimeStampedModel, ActivoMixin):
    """Numeración correlativa de comprobantes por tipo, local y año."""

    tipo_comprobante = models.CharField(
        "tipo de comprobante", max_length=50, choices=TipoComprobante.choices
    )
    prefijo = models.CharField("prefijo", max_length=10, blank=True, default="")
    numero_actual = models.PositiveIntegerField("número actual", default=0)
    local = models.ForeignKey(
        Local,
        on_delete=models.PROTECT,
        related_name="contadores_correlativos",
        verbose_name="local",
    )
    anio = models.PositiveSmallIntegerField("año")

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        verbose_name = "contador correlativo"
        verbose_name_plural = "contadores correlativos"
        db_table = "nucleo.contador_correlativo"
        constraints = [
            models.UniqueConstraint(
                fields=["tipo_comprobante", "local", "anio"],
                name="core_contador_correlativo_uk",
            )
        ]

    def __str__(self):
        return f"{self.tipo_comprobante} - {self.local.codigo} ({self.anio}): {self.numero_actual}"

    @classmethod
    def obtener_siguiente(cls, tipo_comprobante, local, anio=None, prefijo=None):
        """Obtiene e incrementa atómicamente el siguiente correlativo con bloqueo de fila."""
        if anio is None:
            anio = timezone.now().year

        with transaction.atomic():
            contador, _ = cls.objects.select_for_update().get_or_create(
                tipo_comprobante=tipo_comprobante,
                local=local,
                anio=anio,
                defaults={"prefijo": prefijo or "", "numero_actual": 0},
            )
            contador.numero_actual += 1
            if prefijo is not None and contador.prefijo != prefijo:
                contador.prefijo = prefijo
            contador.save(update_fields=["numero_actual", "prefijo", "actualizado_en"])

            prefijo_final = contador.prefijo or tipo_comprobante.upper()[:3]
            return f"{prefijo_final}-{contador.anio}-{contador.numero_actual:06d}"
