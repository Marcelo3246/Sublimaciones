from django.db import models
from core.common.models import Auditable


class Trabajador(Auditable):
    class Estado(models.TextChoices):
        ACTIVO = "activo", "Activo"
        INACTIVO = "inactivo", "Inactivo"

    nombre_completo = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30, blank=True, default="")
    local = models.ForeignKey("identity.Local", on_delete=models.PROTECT, related_name="trabajadores")
    fecha_ingreso = models.DateField()
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVO)
    usuario_id = models.IntegerField(null=True, blank=True, help_text="ID del Usuario del sistema si tiene login")

    class Meta:
        db_table = "hr_trabajador"
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"

    def __str__(self):
        return f"{self.nombre_completo} ({self.local.codigo})"


class PeriodoPlanilla(Auditable):
    tipo_periodo = models.CharField(
        max_length=20,
        choices=[("quincenal", "Quincenal"), ("mensual", "Mensual")],
        default="quincenal",
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=[("abierto", "Abierto"), ("cerrado", "Cerrado")], default="abierto")

    class Meta:
        db_table = "hr_periodo_planilla"
        verbose_name = "Período de Planilla"
        verbose_name_plural = "Períodos de Planilla"

    def __str__(self):
        return f"{self.tipo_periodo}: {self.fecha_inicio} a {self.fecha_fin}"


class Comision(Auditable):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT, related_name="comisiones")
    periodo = models.ForeignKey(PeriodoPlanilla, on_delete=models.SET_NULL, null=True, blank=True, related_name="comisiones")
    pedido_venta_id = models.IntegerField(null=True, blank=True)
    moneda = models.CharField(max_length=3, default="USD")
    valor_liquidado = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    porcentaje_comision = models.DecimalField(max_digits=5, decimal_places=4)
    monto_comision = models.DecimalField(max_digits=14, decimal_places=2)
    origen = models.CharField(max_length=50, blank=True, default="")

    class Meta:
        db_table = "hr_comision"
        indexes = [
            models.Index(fields=["trabajador", "activo"]),
        ]
        verbose_name = "Comisión"
        verbose_name_plural = "Comisiones"

    def __str__(self):
        return f"Comisión {self.trabajador.nombre_completo} - {self.monto_comision} {self.moneda}"


class Adelanto(Auditable):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT, related_name="adelantos")
    monto = models.DecimalField(max_digits=14, decimal_places=2)
    moneda = models.CharField(max_length=3, default="USD")
    fecha = models.DateField()
    comision_origen = models.ForeignKey(Comision, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "hr_adelanto"
        verbose_name = "Adelanto"
        verbose_name_plural = "Adelantos"

    def __str__(self):
        return f"Adelanto {self.trabajador.nombre_completo}: {self.monto} {self.moneda}"


class PagoTrabajador(Auditable):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT, related_name="pagos")
    periodo = models.ForeignKey(PeriodoPlanilla, on_delete=models.SET_NULL, null=True, blank=True)
    moneda = models.CharField(max_length=3, default="USD")
    monto_neto = models.DecimalField(max_digits=14, decimal_places=2)
    metodo = models.CharField(max_length=30, choices=[("efectivo", "Efectivo"), ("transferencia", "Transferencia")], default="transferencia")
    fecha_pago = models.DateField()

    class Meta:
        db_table = "hr_pago_trabajador"
        verbose_name = "Pago a Trabajador"
        verbose_name_plural = "Pagos a Trabajadores"

    def __str__(self):
        return f"Pago {self.trabajador.nombre_completo}: {self.monto_neto} {self.moneda}"
