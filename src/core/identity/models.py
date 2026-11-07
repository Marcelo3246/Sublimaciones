from django.contrib.auth.models import AbstractUser
from django.db import models

from core.common.models import Auditable


# ---------------------------------------------------------------------------
# Local (Sucursal)
# ---------------------------------------------------------------------------

class Local(Auditable):
    """Sucursal / punto de venta del negocio DLL Sublimados.

    TODO (pendiente por implementar):
    - Validación de formato de teléfono.
    - Campos adicionales: correo electrónico, coordenadas GPS, horario.
    """

    nombre = models.CharField(max_length=120)
    codigo = models.CharField(
        max_length=10,
        unique=True,
        help_text="Código corto único del local, ej: 'L01'.",
    )
    direccion = models.TextField(blank=True, default="")
    telefono = models.CharField(max_length=30, blank=True, default="")

    class Meta:
        db_table = "identity_local"
        verbose_name = "Local"
        verbose_name_plural = "Locales"

    def __str__(self):
        return f"{self.codigo} — {self.nombre}"


# ---------------------------------------------------------------------------
# Usuario (modelo de usuario personalizado)
# ---------------------------------------------------------------------------

class Usuario(AbstractUser, Auditable):
    """Modelo de usuario personalizado del sistema DLL Sublimados.

    Extiende ``AbstractUser`` (username, email, password, etc.) y agrega
    campos propios del negocio.

    TODO (pendiente por implementar):
    - Campos de perfil: cédula, teléfono personal, cargo.
    - Método ``tiene_permiso(codigo_permiso, local=None)`` que consulte
      UsuarioRol → RolPermiso para autorización granular.
    - Señal post_save para crear perfil o registros asociados.
    """

    es_global = models.BooleanField(
        default=False,
        help_text="True = el usuario tiene acceso a todos los locales.",
    )
    local_predeterminado = models.ForeignKey(
        Local,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="usuarios_predeterminados",
        help_text="Local que se selecciona por defecto al iniciar sesión.",
    )

    USERNAME_FIELD = "username"

    class Meta:
        db_table = "identity_usuario"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.get_full_name() or self.username


# ---------------------------------------------------------------------------
# Rol
# ---------------------------------------------------------------------------

class Rol(Auditable):
    """Rol de negocio (ej: Administrador, Vendedor, Operador de planta).

    TODO (pendiente por implementar):
    - Jerarquía de roles (rol padre).
    - Validaciones de conflicto de roles.
    """

    codigo = models.CharField(
        max_length=50,
        unique=True,
        help_text="Código único del rol, ej: 'admin', 'vendedor'.",
    )
    nombre = models.CharField(max_length=120)

    class Meta:
        db_table = "identity_rol"
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.nombre


# ---------------------------------------------------------------------------
# Permiso (granular, de negocio)
# ---------------------------------------------------------------------------

class Permiso(Auditable):
    """Permiso granular de negocio, independiente del sistema de permisos
    de Django.

    El código usa formato ``modulo.entidad.accion``, por ejemplo:
    ``inventario.traslado.crear``, ``ventas.factura.anular``.

    TODO (pendiente por implementar):
    - Seeders / fixtures iniciales con los permisos del sistema.
    - Agrupación por módulo para la UI de administración.
    """

    codigo = models.CharField(
        max_length=100,
        unique=True,
        help_text="Formato: modulo.entidad.accion (ej: 'inventario.traslado.crear').",
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, default="")

    class Meta:
        db_table = "identity_permiso"
        verbose_name = "Permiso"
        verbose_name_plural = "Permisos"

    def __str__(self):
        return f"{self.codigo} — {self.nombre}"


# ---------------------------------------------------------------------------
# RolPermiso (muchos a muchos entre Rol y Permiso)
# ---------------------------------------------------------------------------

class RolPermiso(models.Model):
    """Relación muchos-a-muchos entre Rol y Permiso."""

    rol = models.ForeignKey(
        Rol,
        on_delete=models.CASCADE,
        related_name="rol_permisos",
    )
    permiso = models.ForeignKey(
        Permiso,
        on_delete=models.CASCADE,
        related_name="permiso_roles",
    )

    class Meta:
        db_table = "identity_rol_permiso"
        unique_together = [("rol", "permiso")]
        verbose_name = "Rol-Permiso"
        verbose_name_plural = "Roles-Permisos"

    def __str__(self):
        return f"{self.rol.codigo} → {self.permiso.codigo}"


# ---------------------------------------------------------------------------
# UsuarioRol (asignación de rol a usuario, opcionalmente por local)
# ---------------------------------------------------------------------------

class UsuarioRol(models.Model):
    """Asigna un Rol a un Usuario, opcionalmente restringido a un Local.

    Si ``local`` es NULL, el rol aplica globalmente.
    """

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="usuario_roles",
    )
    rol = models.ForeignKey(
        Rol,
        on_delete=models.CASCADE,
        related_name="rol_usuarios",
    )
    local = models.ForeignKey(
        Local,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="local_usuario_roles",
        help_text="NULL = el rol aplica a todos los locales (global).",
    )

    class Meta:
        db_table = "identity_usuario_rol"
        verbose_name = "Usuario-Rol"
        verbose_name_plural = "Usuarios-Roles"

    def __str__(self):
        scope = self.local.codigo if self.local else "GLOBAL"
        return f"{self.usuario.username} — {self.rol.codigo} [{scope}]"


# ---------------------------------------------------------------------------
# UsuarioLocal (locales a los que tiene acceso un usuario)
# ---------------------------------------------------------------------------

class UsuarioLocal(models.Model):
    """Asocia un Usuario con los Locales a los que tiene acceso."""

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="usuario_locales",
    )
    local = models.ForeignKey(
        Local,
        on_delete=models.CASCADE,
        related_name="local_usuarios",
    )

    class Meta:
        db_table = "identity_usuario_local"
        unique_together = [("usuario", "local")]
        verbose_name = "Usuario-Local"
        verbose_name_plural = "Usuarios-Locales"

    def __str__(self):
        return f"{self.usuario.username} ↔ {self.local.codigo}"
