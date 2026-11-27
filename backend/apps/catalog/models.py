"""Modelos de datos del catálogo maestro.

Implementa categorías, subcategorías, unidades de medida, tallas,
materiales, productos, variantes y servicios con class Meta y
db_table explícito (ver docs/tasks/tareas-grupo-base-de-datos.md).
"""

from django.db import models

from backend.apps.catalog.choices import TipoCategoria, TipoProducto
from backend.common.base_models import ActivoMixin, TimeStampedModel


class Categoria(TimeStampedModel, ActivoMixin):
    """Categoría raíz que agrupa materiales, productos o servicios."""

    nombre = models.CharField("nombre", max_length=100)
    tipo = models.CharField(
        "tipo",
        max_length=20,
        choices=TipoCategoria.choices,
        default=TipoCategoria.MATERIAL,
    )

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        db_table = "catalogo.categoria"
        ordering = ["tipo", "nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre", "tipo"],
                name="catalog_categoria_uk",
            ),
            models.CheckConstraint(
                condition=models.Q(tipo__in=TipoCategoria.values),
                name="catalog_categoria_tipo_ck",
            ),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class Subcategoria(TimeStampedModel, ActivoMixin):
    """Subcategoría que refina el dominio de una categoría."""

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="subcategorias",
        verbose_name="categoría",
    )
    nombre = models.CharField("nombre", max_length=100)

    class Meta:
        verbose_name = "subcategoría"
        verbose_name_plural = "subcategorías"
        db_table = "catalogo.subcategoria"
        ordering = ["categoria", "nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["categoria", "nombre"],
                name="catalog_subcategoria_uk",
            )
        ]

    def __str__(self):
        return f"{self.nombre} ({self.categoria.nombre})"


class UnidadMedida(TimeStampedModel, ActivoMixin):
    """Unidad oficial de medida para materiales, servicios y stock."""

    codigo = models.CharField("código", max_length=10)
    nombre = models.CharField("nombre", max_length=50)
    permite_decimales = models.BooleanField("permite decimales", default=True)

    class Meta:
        verbose_name = "unidad de medida"
        verbose_name_plural = "unidades de medida"
        db_table = "catalogo.unidad_medida"
        ordering = ["codigo"]
        constraints = [
            models.UniqueConstraint(
                fields=["codigo"],
                name="catalog_unidad_medida_codigo_uk",
            )
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Talla(TimeStampedModel, ActivoMixin):
    """Talla de producto con su código y orden de presentación."""

    codigo = models.CharField("código", max_length=10)
    nombre = models.CharField("nombre", max_length=50)
    orden = models.PositiveSmallIntegerField("orden", default=0)

    class Meta:
        verbose_name = "talla"
        verbose_name_plural = "tallas"
        db_table = "catalogo.talla"
        ordering = ["orden", "codigo"]
        constraints = [
            models.UniqueConstraint(
                fields=["codigo"],
                name="catalog_talla_codigo_uk",
            )
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Material(TimeStampedModel, ActivoMixin):
    """Materia prima del catálogo (telas, tintas, viniles, papel)."""

    codigo = models.CharField("código", max_length=50)
    nombre = models.CharField("nombre", max_length=150)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="materiales",
        verbose_name="categoría",
    )
    unidad_medida = models.ForeignKey(
        UnidadMedida,
        on_delete=models.PROTECT,
        related_name="materiales",
        verbose_name="unidad de medida",
    )
    es_continuo = models.BooleanField(
        "es continuo",
        default=False,
        help_text="Telas y rollos que se miden por longitud",
    )
    stock_minimo_global = models.DecimalField(
        "stock mínimo global",
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "material"
        verbose_name_plural = "materiales"
        db_table = "catalogo.material"
        ordering = ["nombre"]
        indexes = [
            models.Index(
                fields=["categoria", "activo"],
                name="catalog_material_categoria_idx",
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["codigo"],
                name="catalog_material_codigo_uk",
            )
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Producto(TimeStampedModel, ActivoMixin):
    """Artículo del catálogo: terminado, semiterminado o servicio."""

    codigo = models.CharField("código", max_length=50)
    nombre = models.CharField("nombre", max_length=150)
    descripcion = models.TextField("descripción", blank=True, default="")
    subcategoria = models.ForeignKey(
        Subcategoria,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="productos",
        verbose_name="subcategoría",
    )
    tipo = models.CharField(
        "tipo",
        max_length=20,
        choices=TipoProducto.choices,
        default=TipoProducto.TERMINADO,
    )

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"
        db_table = "catalogo.producto"
        ordering = ["nombre"]
        indexes = [
            models.Index(
                fields=["subcategoria", "activo"],
                name="catalog_producto_subcat_idx",
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["codigo"],
                name="catalog_producto_codigo_uk",
            ),
            models.CheckConstraint(
                condition=models.Q(tipo__in=TipoProducto.values),
                name="catalog_producto_tipo_ck",
            ),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class VarianteProducto(TimeStampedModel, ActivoMixin):
    """Variante stockeable de un producto (talla y color)."""

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="variantes",
        verbose_name="producto",
    )
    talla = models.ForeignKey(
        Talla,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="variantes",
        verbose_name="talla",
    )
    color = models.CharField("color", max_length=50, blank=True, default="")
    sku = models.CharField("SKU", max_length=30)
    codigo_barras = models.CharField(
        "código de barras", max_length=50, blank=True, default=""
    )

    class Meta:
        verbose_name = "variante de producto"
        verbose_name_plural = "variantes de producto"
        db_table = "catalogo.variante_producto"
        ordering = ["producto", "sku"]
        constraints = [
            models.UniqueConstraint(
                fields=["sku"],
                name="catalog_variante_producto_sku_uk",
            ),
            models.UniqueConstraint(
                fields=["producto", "talla"],
                name="catalog_variante_uk",
            ),
        ]

    def __str__(self):
        return f"{self.sku} - {self.producto.nombre}"


class Servicio(TimeStampedModel, ActivoMixin):
    """Servicio ofrecido por el negocio (sublimación, confección, etc.)."""

    nombre = models.CharField("nombre", max_length=150)
    descripcion = models.TextField("descripción", blank=True, default="")
    unidad_medida = models.ForeignKey(
        UnidadMedida,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="servicios",
        verbose_name="unidad de medida",
    )

    class Meta:
        verbose_name = "servicio"
        verbose_name_plural = "servicios"
        db_table = "catalogo.servicio"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
