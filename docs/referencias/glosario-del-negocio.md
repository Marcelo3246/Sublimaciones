---
status: borrador
type: nota
tags:
  - glosario
  - negocio
created: 2026-11-04
---

# Glosario del negocio

Términos que uses igual en toda la especificación. Si un término no está aquí, se define antes de usarlo en un requerimiento.

## Términos de organización

| Término | Definición |
| --- | --- |
| Local | Cada una de las 3 sedes físicas del negocio. Contexto operativo y de inventario. Toda transacción pertenece a uno. |
| Local principal | Sede donde se realiza impresión y corte. Abastece a los otros locales. |
| Operador | Usuario limitado a un local, con roles sobre módulos específicos. |
| Usuario global | Usuario (dueño, admin, gerencial) con alcance sobre todos los locales. |

## Términos de catálogo y materiales

| Término | Definición |
| --- | --- |
| Materia prima | Material de entrada: tela, vinil, papel de sublimación, tinta, tazas, franelas. |
| Producto | Artículo de venta final o intermedio: franela sublimada, taza personalizada, combo. |
| Servicio | Trabajo cobrado al cliente: sublimación, planchado, confección, diseño. |
| Diseño | Arte digital (logo, imagen) preparado por el diseñador de forma externa al sistema para alimentar la impresión. |
| Unidad de medida (UM) | Forma de medir material: metro, metro cuadrado, litro, gramo, unidad. |
| Talla | Variante de medida aplicable a prendas: S, M, L, XL. |
| Categoría / Subcategoría | Clasificación jerárquica de materiales, productos y servicios. La subcategoría está diseñada pero sin uso en fase 1. |

## Términos de inventario

| Término | Definición |
| --- | --- |
| Rollo / lote (batch) | Objeto físico trazable de material continuo (tela, vinil, papel): un rollo con su `codigo_lote`, longitud inicial y sobrante. Término antes llamado "partida". |
| Stock | Saldo agregado (disponible y reservado) por material o variante en cada local; es lo que ven las pantallas de inventario. Cada local opera su propio stock. |
| Medición | Consumo registrado sobre un lote, p. ej. 1.8 m de un lote de 10 m. |
| Sobrante | Longitud remanente de un rollo tras consumos. Reutilizable si supera el mínimo aprovechable. |
| Desperdicio (merma) | Material perdido por error de producción, rayado, falla de impresión. Genera un movimiento de salida por desperdicio. |
| Estado del material | Condición del stock: disponible, dañado, reservado, en tránsito. |
| Transferencia | Movimiento de stock entre locales, con guía interna que descuenta en origen y entra en destino. |
| Valorización | Costo atribuido al stock: promedio ponderado de entradas. Alimenta precios y costos de producción. |

## Términos de ventas y precios

| Término | Definición |
| --- | --- |
| Matriz de precios | Tabla que define el precio base por combinación de producto / servicio / material / medida. |
| Fórmula de precio | Precio final = precio base × 1.30 (margen) × 1.16 (impuesto). Orden validado en la sesión de requerimientos. |
| Pedido | Orden de trabajo de un cliente. Distintas vistas de la misma entidad de venta. |
| Factura propia | Documento de venta interno, numeración correlativa por local. |
| Nota de entrega | Documento que acompaña la entrega física sin ser factura. |
| Comisión | Porcentaje del valor liquidado de una venta asignado al trabajador que la generó. |

## Términos de producción

| Término | Definición |
| --- | --- |
| Orden de producción | Encargo interno que descompone un pedido en pasos por local. |
| Ruta de producción | Secuencia de pasos por local: impresión, corte (local principal); planchado, confección, diseño (locales secundarios). |
| Operación de máquina | Registro de cada uso de una máquina: máquina, operador, duración, resultado. |
| Consumo por medición | Salida de material de un lote, medida en su UM, dentro de una orden de producción. |

## Términos de sistema

| Término | Definición |
| --- | --- |
| Monolito modular | Una sola aplicación Django con módulos `apps` internos de límites explícitos. |
| Módulo (app) | Unidad de negocio acotada en código con modelo, servicios y vistas propios. |
| Traspaso entre módulos | Llamada a la capa de servicio del otro módulo, nunca a su ORM interno. |
| Bitácora (log) | Registro append-only de acciones: de usuario (quién, qué, cuándo, antes/después) y de stock (todo cambio de inventario). |
| Cargo | Rol operativo de un trabajador en el negocio. Valores: `impresor`, `vendedor`, `disenador`, `planchador`, `confeccionador`. Usado para asignar pasos de producción. |

## Referencias

- [Monolito modular](monolito-modular.md)