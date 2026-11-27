---
status: borrador
type: documento
tags:
  - ddl
  - sql
  - postgresql
  - base-de-datos
  - especificacion
created: 2026-11-09
version: 0.3
---

# 06b Esquemas y DDL PostgreSQL

DDL canónico del modelo de [06 Modelo de datos](06-modelo-de-datos.md), agrupado por esquema (un esquema de PostgreSQL por módulo Django). Sirve como referencia de revisión y para montar la base de desarrollo; **en producción lo genera Django** vía migraciones (`Meta.db_table` con nombre calificado por esquema, p. ej. `ventas.pedido_venta`) — el orden de las notas replica el orden de aplicación de las migraciones.

Cada esquema tiene su propia nota con el SQL completo. Esta nota es el **índice** y el resumen de las reglas comunes.

## Reglas resumidas

- Montos `NUMERIC(14,2)` + `moneda` (`USD` | `VES`); cantidades `NUMERIC(12,4)`; porcentajes `NUMERIC(5,4)`.
- Estados y opciones cerradas con `CHECK` en BD y `TextChoices` en Django.
- Booleanos de negocio en español (`activo`, `es_global`, `es_principal`, `es_predeterminada`); borrado lógico con `activo = false`.
- FK con el patrón `<entidad>_id`.
- Convención completa en [07 Convenciones de base de datos](07-convenciones-de-base-de-datos.md).

## Bloque común (`TimeStampedModel` + `ActivoMixin`)

Toda tabla de negocio hereda estos mixins abstractos de `backend/common/base_models.py`:

```sql
creado_en      TIMESTAMPTZ NOT NULL DEFAULT now(),
actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
activo         BOOLEAN NOT NULL DEFAULT true
```

Las bitácoras de `auditoria` solo llevan `creado_en` (append-only: sin `UPDATE`, sin `DELETE`, sin `activo`). `documentos.documento` hereda únicamente `TimeStampedModel` (usa `estado`: `'generado'` | `'anulado'`).

## Índice de esquemas

| # | Esquema | Nota del DDL | Modelo | Tablas |
| --- | --- | --- | --- | --- |
| 1 | `nucleo` | [06b.1 nucleo](ddl/06b.1-nucleo.md) | [06.1 nucleo](modelo-datos/06.1-nucleo.md) | local, usuario (+ usuario_groups, usuario_user_permissions), tasa_cambio, contador_correlativo |
| 2 | `auditoria` | [06b.2 auditoria](ddl/06b.2-auditoria.md) | [06.2 auditoria](modelo-datos/06.2-auditoria.md) | bitacora_accion, bitacora_stock |
| 3 | `catalogo` | [06b.3 catalogo](ddl/06b.3-catalogo.md) | [06.3 catalogo](modelo-datos/06.3-catalogo.md) | categoria, subcategoria, unidad_medida, talla, material, producto, variante_producto, servicio |
| 4 | `inventario` | [06b.4 inventario](ddl/06b.4-inventario.md) | [06.4 inventario](modelo-datos/06.4-inventario.md) | stock, lote, movimiento_stock, guia_transferencia, linea_guia_transferencia, nivel_minimo |
| 5 | `compras` | [06b.5 compras](ddl/06b.5-compras.md) | [06.5 compras](modelo-datos/06.5-compras.md) | empresa, proveedor, orden_compra, linea_orden_compra, recepcion_compra, linea_recepcion_compra, factura_compra, historial_precio_proveedor |
| 6 | `produccion` | [06b.6 produccion](ddl/06b.6-produccion.md) | [06.6 produccion](modelo-datos/06.6-produccion.md) | orden_produccion, paso_produccion, consumo_material, maquina, operacion_maquina |
| 7 | `ventas` | [06b.7 ventas](ddl/06b.7-ventas.md) | [06.7 ventas](modelo-datos/06.7-ventas.md) | cliente, pedido_venta, linea_pedido, cobro, factura |
| 8 | `precios` | [06b.8 precios](ddl/06b.8-precios.md) | [06.8 precios](modelo-datos/06.8-precios.md) | item_matriz_precios, historial_cambio_precio, parametro_formula |
| 9 | `rrhh` | [06b.9 rrhh](ddl/06b.9-rrhh.md) | [06.9 rrhh](modelo-datos/06.9-rrhh.md) | trabajador, trabajador_local |
| 10 | `documentos` | [06b.10 documentos](ddl/06b.10-documentos.md) | [06.10 documentos](modelo-datos/06.10-documentos.md) | plantilla_documento, documento |
| 11 | — | [06b.11 reports](ddl/06b.11-reports.md) | [06.11 reports](modelo-datos/06.11-reports.md) | sin tablas: el módulo `reports` solo consulta |

## Orden de aplicación de las migraciones

Las dependencias entre esquemas fijan el orden en que las apps deben aplicar sus migraciones:

```text
nucleo → catalogo → inventario → auditoria
                     → compras
                     → produccion → rrhh
                     → ventas → precios → documentos
```

## Referencias

- [06 Modelo de datos](06-modelo-de-datos.md)
- [07 Convenciones de base de datos](07-convenciones-de-base-de-datos.md)
- [Monolito modular](referencias/monolito-modular.md)
- [Glosario](referencias/glosario-del-negocio.md)
