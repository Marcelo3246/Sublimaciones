from django.db import models
from core.common.models import Auditable


class Categoria(Auditable):
    class Tipo(models.TextChoices):
        MATERIAL = "material", "Materia Prima"
        PRODUCTO = "producto", "Producto Terminado"
        SERVICIO = "servicio", "Servicio"

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)

    class Meta:
        db_table = "catalog_categoria"
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class Subcategoria(Auditable):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="subcategorias")
    nombre = models.CharField(max_length=100)
    en_uso = models.BooleanField(default=False, help_text="Indica si actualmente se utiliza")

    class Meta:
        db_table = "catalog_subcategoria"
        verbose_name = "Subcategoría"
        verbose_name_plural = "Subcategorías"

    def __str__(self):
        return f"{self.categoria.nombre} > {self.nombre}"


class UnidadMedida(Auditable):
    class Tipo(models.TextChoices):
        LONGITUD = "longitud", "Longitud (m, cm)"
        AREA = "area", "Área (m²)"
        VOLUMEN = "volumen", "Volumen (L, ml)"
        MASA = "masa", "Masa (kg, g)"
        UNIDAD = "unidad", "Unidad contable"

    codigo = models.CharField(max_length=20, unique=True, help_text="m, m2, l, kg, und")
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)

    class Meta:
        db_table = "catalog_unidad_medida"
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class Talla(Auditable):
    class Tipo(models.TextChoices):
        ALFANUMERICA = "alfanumerica", "Alfanumérica (S, M, L, XL)"
        NUMERICA = "numerica", "Numérica (38, 40, 42)"

    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.ALFANUMERICA)

    class Meta:
        db_table = "catalog_talla"
        verbose_name = "Talla"
        verbose_name_plural = "Tallas"

    def __str__(self):
        return self.nombre


class Material(Auditable):
    class FormatoStock(models.TextChoices):
        CONTINUO = "continuo", "Continuo (rollo, bobina, medido)"
        CONTABLE = "contable", "Contable (piezas, láminas, unidades)"

    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="materiales")
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_medicion = models.CharField(max_length=20, choices=UnidadMedida.Tipo.choices)
    formato_stock = models.CharField(max_length=20, choices=FormatoStock.choices, default=FormatoStock.CONTINUO)
    um_predeterminada = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, related_name="materiales_principales")
    sobrante_minimo = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=0,
        help_text="Mínimo aprovechable antes de considerarse desperdicio (RF-15)",
    )

    class Meta:
        db_table = "catalog_material"
        verbose_name = "Material"
        verbose_name_plural = "Materiales"

    def __str__(self):
        return self.nombre


class Producto(Auditable):
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos")
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=50, blank=True, default="")

    class Meta:
        db_table = "catalog_producto"
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre


class VarianteProducto(Auditable):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="variantes")
    talla = models.ForeignKey(Talla, on_delete=models.PROTECT, null=True, blank=True)
    sku = models.CharField(max_length=50, unique=True)
    longitud_estandar_material = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Consumo de tela/vinil estándar para esta variante",
    )

    class Meta:
        db_table = "catalog_variante_producto"
        verbose_name = "Variante de Producto"
        verbose_name_plural = "Variantes de Producto"

    def __str__(self):
        return f"{self.producto.nombre} - SKU: {self.sku}"


class Servicio(Auditable):
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="servicios")
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True, blank=True)
    um_predeterminada = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        db_table = "catalog_servicio"
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return self.nombre


class Diseno(Auditable):
    nombre = models.CharField(max_length=150)
    ruta_archivo = models.FileField(upload_to="disenos/", blank=True, null=True)
    version = models.IntegerField(default=1)

    class Meta:
        db_table = "catalog_diseno"
        verbose_name = "Diseño"
        verbose_name_plural = "Diseños"

    def __str__(self):
        return f"{self.nombre} v{self.version}"
