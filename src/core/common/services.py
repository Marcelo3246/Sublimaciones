"""
core.common.services
====================

Funciones de utilidad transversales al sistema DLL Sublimados.

Pendiente por implementar:
--------------------------

get_tasa_cambio_del_dia(fecha=None)
    Retorna la TasaCambio vigente para la fecha indicada (o la de hoy si no
    se especifica).  Debe lanzar una excepción clara si no existe tasa
    registrada para ese día.

generar_secuencia_correlativa(tipo, local, año)
    Genera el próximo número correlativo (ej. "OT-L01-2025-00042") de forma
    atómica (SELECT … FOR UPDATE o F-expressions) para evitar colisiones
    concurrentes.  ``tipo`` indica la entidad (orden_trabajo, factura, etc.),
    ``local`` es el código de la sucursal, y ``año`` el ejercicio fiscal.
"""
