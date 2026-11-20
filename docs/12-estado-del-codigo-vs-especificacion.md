---
status: borrador
type: documento
tags:
  - divergencias
  - codigo
  - especificacion
  - trazabilidad
created: 2026-11-15
version: 0.1
---

# 12 Estado del código vs especificación

Qué parte de la especificación de [03 Requerimientos del sistema](03-requerimientos-del-sistema.md) y [06 Modelo de datos](06-modelo-de-datos.md) está implementada en el repositorio, qué parte no, y en qué dirección se resuelve cada diferencia. Sirve para que nadie lea la especificación y dé por hecho que el código ya la cumple.

## Cómo leer esta nota

- **Especificación**: lo que dice la documentación de este vault (modelo de datos, DDL y requerimientos).
- **Código**: lo que hoy hay en `src/` del repositorio.
- **Acción**: hacia dónde se resuelve. `Spec` = se ajusta la documentación. `Código` = se ajusta el código. `Decidir` = requiere una decisión del Grupo de Gestión.

## Divergencias de infraestructura

| Tema | Especificación | Código actual | Acción |
| --- | --- | --- | --- |
| Estructura del proyecto | Monolito modular Django + React | Conforme: `manage.py` en la raíz, backend en `backend/apps/` (estándar OptiRosse) | — |
| Aislamiento de datos | Uso de `class Meta` con `db_table` por módulo | Encomendado al Grupo de Base de Datos según normativa | Código (Grupo BD) |
| Versionado de Django | Django 5+ (RNF-02) | `Django>=6.0,<7.0` en `requirements.txt` | Spec |
| Frontend | SPA React + Vite + Tailwind en `frontend/` | Conforme: creado en `frontend/` con 11 features, layout, providers y servicios | — |
| Scripts SQL | `database/` con scripts de arranque | Conforme: `00_crear_bd.sql` y `01_datos_iniciales.sql` | — |
| Pruebas | `tests/` con pruebas unitarias | Configurado con pytest en `backend/apps/core/tests.py` | — |
| Estructura de la API | Cada módulo expone `api.py` | Resuelto: se adopta convención DRF estándar (`views.py` + `urls.py` + `serializers.py`) | Spec |
| Frontend de la SPA | `frontend/src/features/<modulo>/` | Conforme: 11 carpetas modulares con api, pages, components, hooks y types | — |
| Entorno virtual | `venv/` ignorado, solo `requirements.txt` versionado | Conforme | — |

## Divergencias del modelo de datos

### Identidad y núcleo

| Tema | Especificación | Código actual | Acción |
| --- | --- | --- | --- |
| Alcance global | Campo `is_global` | Campo `es_global` | Decidir |
| Borrado lógico | Campo `is_active` en el mixin `Auditable` | Campo `activo` | Decidir |
| Permisos | Matriz granular **en código** (`permissions.py`), sin tablas de permisos | Existen `identity_permiso` e `identity_rol_permiso` en base de datos | Decidir |
| Numeración correlativa | `nucleo.contador_correlativo` con bloqueo de fila (RF-54) | No existe el modelo | Código |
| Tipo de cambio | Tabla `nucleo.tasa_cambio` | Tabla `common_tasa_cambio`, en `core.common` | Spec |
| Jerarquía de personas | `Persona` como clase base de `Usuario`, `Cliente` y `Proveedor` (norma del proyecto, ver [11 Normas de código y POO](11-normas-de-codigo-y-poo.md)) | No existe la clase base | Código |

### Auditoría

| Tema | Especificación | Código actual | Acción |
| --- | --- | --- | --- |
| Referencia al objeto auditado | `entidad_tipo` + `entidad_id` | `entidad` (texto) + `entidad_id` | Decidir |
| Referencia al lote | `bitacora_stock` con `lote_id` y `tipo_item` | Implementada con `tipo_item` e `item_id` | Spec |

### Catálogo

| Tema | Especificación | Código actual | Acción |
| --- | --- | --- | --- |
| Diseños digitales | RF-12 los deja **fuera** del sistema, gestionados por el diseñador | Existe `catalog_diseno` y `OrdenProduccion.diseno` | Decidir |
| Medida en la matriz | `medida_cantidad` + `um_medida_id` (numérico, comparable) | `medida` como texto libre + `talla` como FK | Código |

### Inventario

| Tema | Especificación | Código actual | Acción |
| --- | --- | --- | --- |
| Nombre de la entidad de saldo | `Stock` (`inventario.stock`) | `Existencia` (`inventory_existencia`) | Decidir |
| Nombre del objeto trazable | `Lote` (`inventario.lote`) | `Partida` (`inventory_partida`) | Decidir |
| Unidad de medida | FK a `catalogo.unidad_medida` | Texto libre (`um = "m"`) | Código |
| Saldo reservado | `cantidad_reservada` en el saldo | No existe | Código |
| Cantidad restante | `lote.cantidad_actual` | `partida.cantidad_restante` | Decidir |
| Caducidad y costo del lote | `fecha_vencimiento`, `costo_unitario`, `moneda` | No existen | Código |
| Valorización | Valorización por promedio ponderado (RF-23) | Sin campos de costo | Código |
| Stock de producto | Apunta a la **variante** (para no perder la talla) | Apunta al `Producto` | Código |
| Nivel mínimo por local | `inventario.nivel_minimo` (RF-24) | No existe | Código |
| Transferencias | Guía con líneas y estados por línea | `GuiaTransferencia` existe, sin líneas ni estados por línea | Código |

### Compras

| Tema | Especificación | Código actual | Acción |
| --- | --- | --- | --- |
| Empresa y proveedor | `compras.empresa` + `compras.proveedor` | Solo `Proveedor` | Código |
| Recepción de compra | `RecepcionCompra` + `LineaRecepcionCompra`, con entradas parciales | No existen | Código |
| Historial de precios | Historial por material, proveedor y fecha | Existe `HistorialPrecioProveedor` | Spec |

### Producción

| Tema | Especificación | Código actual | Acción |
| --- | --- | --- | --- |
| Estados de la orden | `creada`, `en_produccion`, `terminada`, `anulada` | `planificada`, `en_proceso`, `terminada`, `anulada` | Decidir |
| Producto a fabricar | `variante_id` (FK a `VarianteProducto`) | No hay producto ni cantidad en la orden | Código |
| Ruta multi-local | `PasoProduccion` con `orden_paso`, `tipo_paso` y local | Existe `PasoProduccion` | Spec |
| Consumo | Apunta a lote **o** a stock del material contable | Apunta siempre a `Partida` | Código |
| Costo de ejecución | `costo_materiales`, `costo_horas`, `costo_total` al cierre (RF-35) | No existen | Código |

### Ventas

| Tema | Especificación | Código actual | Acción |
| --- | --- | --- | --- |
| Cliente del pedido | Obligatorio (nunca queda huérfano, RF-36) | `null=True` | Código |
| Cobro | Entidad `ventas.cobro` con método, referencia, tasa aplicada y cobros parciales (RF-42) | Campo `tipo_cobro` dentro de `PedidoVenta`; no hay cobros parciales | Código |
| Anulación | `motivo_anulacion` obligatorio al anular (RF-43) | No existe | Código |
| Número de factura | Correlativo por (local, año) | `numero_factura` único global | Código |
| Precio en la línea | Snapshot del precio + referencia débil al ítem de la matriz (RF-39) | Snapshot sin referencia al ítem | Código |

### Precios

| Tema | Especificación | Código actual | Acción |
| --- | --- | --- | --- |
| Fórmula | `base × 1.30 × 1.16` | `porcentaje_margen = 1.3000`, `porcentaje_iva = 0.1600` → `base × margen × (1 + iva)` | Conforme |
| Parametrización por vigencia | `precios.parametro_formula` con `fecha_desde` / `fecha_hasta` (RF-45) | No existe; los porcentajes viven en cada fila | Código |
| Exclusión de destinos | CHECK: producto, variante o servicio, nunca dos | No hay `VarianteProducto` en la matriz | Código |

### Recursos humanos

| Tema | Especificación | Código actual | Acción |
| --- | --- | --- | --- |
| Nómina y comisiones | **Diferida** a la fase 4 (RF-49–RF-51) | `PeriodoPlanilla`, `Comision`, `Adelanto`, `PagoTrabajador` ya implementados | Decidir |
| Asignación por local | `TrabajadorLocal` con `is_principal` | No existe la tabla de asignación | Código |

## Elementos de la especificación aún no implementados

Resumen ejecutivo de lo que falta:

| Área | Pendiente |
| --- | --- |
| Inventario | Nivel mínimo por local, saldo reservado, valorización por costo promedio, guía de transferencia con líneas |
| Ventas | Entidad de cobro con multi-moneda y cobros parciales, motivo de anulación, correlativo de factura por local y año |
| Compras | Empresa, recepción de compra con lotes generados |
| Producción | Producto, cantidad y ruta en la orden; costos de ejecución al cierre |
| Precios | Parámetros de fórmula con vigencia por fechas |
| Core | Contador correlativo con bloqueo de fila |
| Identidad | Clase base `Persona` |
| Transversal | Frontend SPA, scripts SQL en `database/`, pruebas en `tests/` |

## Elementos del código que la especificación no contempla

| Elemento | Dónde | Por qué hay que decidirlo |
| --- | --- | --- |
| Tablas de permisos en base de datos | `identity_permiso`, `identity_rol_permiso` | La arquitectura fijó la matriz de permisos en código, sin migraciones por cada cambio funcional |
| Diseño digital | `catalog_diseno`, `production_orden_produccion.diseno` | RF-12 lo saca del sistema; el código lo metió |
| Nómina completa | `hr_periodo_planilla`, `hr_comision`, `hr_adelanto`, `hr_pago_trabajador` | La especificación la difiere a la fase 4 |
| Estados de la orden de producción | `planificada` / `en_proceso` | La especificación usa `creada` / `en_produccion` |
| Nombre `Partida` | `inventory_partida` | El glosario ya lo trata como nombre antiguo de `Lote` |
| Nombre `Existencia` | `inventory_existencia` | Alternativa a `Stock` |

## Plan de convergencia

| Fase | Objetivo | Impacto |
| --- | --- | --- |
| **A — Nomenclatura** | Fijar los nombres canónicos: `is_active`/`activo`, `is_global`/`es_global`, `Lote`/`Partida`, `Stock`/`Existencia`, estados de la orden de producción | Renombrados en modelos y migraciones; sin cambio de comportamiento |
| **B — Aislamiento** | Decidir entre esquemas PostgreSQL por módulo y tablas planas con prefijo | Si se adoptan esquemas: `Meta.db_table` calificado y orden de migraciones por dependencia |
| **C — Reglas de negocio** | Implementar los pendientes de la tabla anterior (nivel mínimo, cobro, recepción, correlativos, costos, fórmula parametrizada) | Es el grueso del trabajo funcional de los equipos |
| **D — Permisos** | Decidir si la matriz de permisos vive en código o en base de datos, y alinear la arquitectura | Afecta a `core.identity` y a la vista del frontend |
| **E — Nómina y diseños** | Activar la fase 4 o revertir el código de nómina y de diseños a lo especificado | Decisión de alcance del cliente |
| **F — Entorno completo** | Frontend SPA, scripts SQL en `database/` y pruebas en `tests/` | Cierra el RNF-06 (backups) y el RNF-07 (latencia) |

## Referencias
- [03 Requerimientos del sistema](03-requerimientos-del-sistema.md)
- [06 Modelo de datos](06-modelo-de-datos.md)
- [07 Convenciones de base de datos](07-convenciones-de-base-de-datos.md)
- [09 Decisiones diferidas y fases](09-decisiones-diferidas-y-fases.md)
- [11 Normas de código y POO](11-normas-de-codigo-y-poo.md)
- [10 Git Flow y normas del equipo](10-git-flow-y-normas-del-equipo.md)
- [Glosario](referencias/glosario-del-negocio.md)
