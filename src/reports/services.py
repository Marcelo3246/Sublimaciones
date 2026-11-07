"""Servicios de agregación y KPIs para el dashboard y reportes."""


def dashboard_ventas_dia(local_id=None):
    """KPIs de ventas del día por local o consolidado global."""
    # TODO: Consultar PedidoVenta filtrado por fecha y local
    pass


def reporte_ventas_por_local(fecha_inicio, fecha_fin):
    """Ventas agrupadas por local en un rango de fechas."""
    pass


def comparativa_proveedores(material_id):
    """Historial y comparativa de precios del material entre proveedores."""
    pass


def giro_inventario(local_id=None):
    """Rotación de materiales y productos por local."""
    pass


def desempeno_maquinas(local_id=None):
    """Horas operativas y desperdicio registrado por máquina."""
    pass


def reporte_comisiones(periodo_id):
    """Resumen de comisiones del período por trabajador."""
    pass
