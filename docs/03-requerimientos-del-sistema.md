---
status: borrador
type: documento
tags:
  - requerimientos
  - especificacion
created: 2026-11-04
version: 0.3
---

# 03 Requerimientos del sistema

Requerimientos funcionales (RF) y no funcionales (RNF) depurados y numerados, con la trazabilidad hacia la lista cruda original. Los términos usados aquí están definidos en [Glosario](referencias/glosario-del-negocio.md).

## Constantes que cruzan todos los RF

- Toda transacción (stock, venta, compra, producción, transferencia, comisión) pertenece a un **local**.
- Todo cambio de negocio genera registro en la **bitácora** del módulo `audit`.
- Los montos son **multi-moneda**: la moneda de referencia es USD; el sistema guarda el tipo de cambio del día y expresa valores en moneda local cuando corresponde.
- El **modelo de datos va en español** (tablas, columnas, estados): `lote`, `cantidad_actual`, `precio_unitario`. La lógica de código que no es modelo (funciones, servicios, componentes de React) va en inglés. La interfaz, también en español neutro.

---

## RF por módulo

### 1. identity — Login, registro y usuarios

| ID | Requerimiento | Origen (crudo) |
| --- | --- | --- |
| RF-01 | Autorización y autenticación de usuarios con sesión segura (cookie firmada y CSRF). Login y SignUp en dos vistas del mismo módulo | "Módulo Login – Sign Up" |
| RF-02 | Roles en BD con alcance por un solo local (operarios, gerentes) o global (dueño, admin, gerencia) (modelo mixto); matriz de permisos por rol definida en código del backend | "Usuarios con alcance por local" |
| RF-03 | Página de perfil y **configuración de usuario**: cambiar contraseña, datos personales, preferencias de vista (local por defecto) | "Módulo de Configuración de Usuario" |
| RF-04 | CRUD de locales y de sus datos de contacto; asignación usuario-local | "Locales y trabajadores" |
| RF-05 | Bloqueo de traslado de tareas a locales no asignados, aplicado a nivel de permisos | "Mixto" |

### 2. audit — Auditoría y panel de admin

| ID | Requerimiento | Origen (crudo) |
| --- | --- | --- |
| RF-06 | Bitácora **append-only** de acciones de usuario: quién, qué entidad/instancia, qué hizo, valores antes/después, fecha-hora, IP | "Hist. movimientos de usuarios" + "Panel de Admin (Auditoría)" |
| RF-07 | Bitácora de movimientos de stock: cada entrada, salida, ajuste, transferencia o cambio de estado, referida al lote o stock-item afectado | "Hist. movimientos de stock" |
| RF-08 | Dos vistas del mismo dominio: bitácora de usuario y bitácora de stock, con filtros (local, fecha, usuario, módulo) | "Mismo módulo, diferentes vistas" |
| RF-09 | **Panel de administración** con: dashboard de auditoría, gestión de bitácoras, reporte exportable (CSV/PDF) | "Panel de Admin (Auditoría)" |

### 3. catalog — Dominios y atributos

| ID | Requerimiento | Origen (crudo) |
| --- | --- | --- |
| RF-10 | CRUD de **materia prima**, **producto** y **servicio**, cada uno con categoría y subcategoría (opcional, hecha para el futuro) | "Gestión de productos por categoría y subcategorías" |
| RF-11 | CRUD de **unidades de medida** (metro, m², litro, gramo, unidad) y **tallas** (S, M, L, XL, numéricas) | "Gestión de unidades de medida y tallas" |
| RF-12 | *(excluido del sistema)* Gestión de diseños y artes digitales: administrada de forma externa directamente por el diseñador | "Gestión de diseños" |
| RF-14 | **Formato de abastecimiento** por material: continuo (rollo, m², volumen, masa) o contable (unidad, lámina); define la regla de consumo | "Materias primas" (varias entradas crudas) |
| RF-15 | UM base mínima aprovechable por material (p. ej. rollo con sobrante mínimo 30 cm) para decidir si el sobrante se reutiliza o se marca como desperdicio | "Conceptos de rollo/sobrante" |

### 4. inventory — Stock multi-local

| ID | Requerimiento | Origen (crudo) |
| --- | --- | --- |
| RF-13 | **Estado del material** (disponible, dañado, reservado, en tránsito) como campo de lote/stock, no tabla aparte | "Estados del material (Dañado, etc)" |
| RF-16 | Stock por local: stock disponible por material (con formato continuo) o producto (por unidad), en una misma entidad base con el campo `tipo: material|producto`. **Por defecto cada local solo ve y opera su propio stock**; los usuarios globales cambian de local o ven el consolidado | "Inventario (vista productos / vista materia prima)" |
| RF-17 | Dos vistas sobre el mismo módulo: vista de productos y vista de materia prima | "Mismo módulo, diferentes vistas" |
| RF-18 | **Entradas con trazabilidad por lote (batch/rollo)** para formatos continuos: longitud/área inicial, instalada desde una entrada (directa, por compra, por transferencia, por devolución) | "Stock entre locales" + "Materiales en productos" |
| RF-19 | **Consumo por medición**: modelo registra descuentos sobre lotes continuos; sobre lotes contables, x unidades; lotes con caducidad generan estado descartable automático | "Gestión de producción (salidas de material por medidas)" |
| RF-20 | Chequeo de mínimo: rollos con sobrante por debajo del mínimo aprovechable se marcan como **desperdicio** y consolidan su estado | "Desperdicio de materiales" |
| RF-21 | **Transferencias entre locales**: solicitudes con guía interna, código de seguimiento y estado (solicitada, despachada, en tránsito, recibida); afecta entradas y salidas en ambos lados | "Gestión de stock entre locales" |
| RF-22 | Estados híbridos por lote: consignados, en tránsito (entre locales), reservados para una orden, dañados, vencidos | "Estados del material" |
| RF-23 | Valorización por promedio ponderado (FIFO-consistent) del costo de inventario, alimentando precios y costos de producción | "Contabilidad del material" |
| RF-24 | Listas de estados del lote y del stock, con alerta de niveles mínimos por material | "Estados del material (Dañado)" |

### 5. purchasing — Compras y proveedores

| ID | Requerimiento | Origen (crudo) |
| --- | --- | --- |
| RF-25 | CRUD de **proveedores** con datos de contacto, condiciones de pago y listado histórico de compras | "Módulo de Proveedores" |
| RF-26 | Órdenes de compra y su recepción: genera entrada de stock al local que compra | "Módulo de Compras" |
| RF-27 | Facturas de compra por proveedor y fecha, con imagen/PDF adjunto | "Facturas de compra" |
| RF-28 | **Comparador de precios por proveedor**: historial de precio material+UM por proveedor y fecha, mostrando el más bajo, con alerta de estables o flotantes (anomalías) | "Comparación de precios por proveedores" |
| RF-29 | Compras en la moneda elegida (USD o Bs.), con conversión por el tipo de cambio del día y registro en bitácora de auditoría | "Multi-moneda" |

### 6. production — Producción multi-local

| ID | Requerimiento | Origen (crudo) |
| --- | --- | --- |
| RF-30 | **Orden de producción** creada desde un pedido o de forma directa, con producto, cantidad y medidas/tallas | "Gestión de producción de productos" |
| RF-31 | **Ruta multi-local**: pasos encadenados por local (impresión y corte en L1; planchado, confección y diseño en L2/L3), con estado por paso (pendiente, en proceso, terminado) | "Producción con locales" |
| RF-32 | Registrar **consumo de material por medición** en cada paso, sobre el lote específico | "Salidas de material por medidas" |
| RF-33 | Registro de **operaciones por máquina**: máquina, operador, duración y resultado; base para indicadores de eficiencia futuros | "Gestión de operaciones realizadas por máquina" |
| RF-34 | Registrar **desperdicio** separado del consumo útil, con motivo (impresión fallida, error de corte, merma de corte térmico, etc.) | "Estados del material" |
| RF-35 | Al terminar la orden: **entrada del producto terminado al stock del último local** + reporte de costo de ejecución (materiales + horas) | "Producción -> ventas" |

### 7. sales — Clientes, pedidos y facturación propia

| ID | Requerimiento | Origen (crudo) |
| --- | --- | --- |
| RF-36 | CRUD de **clientes** con datos de contacto e histórico de pedidos por local | "Módulo de Clientes" |
| RF-37 | **Pedido** con líneas (producto, servicio, material, medida, talla, cantidad), estados (cotizado, confirmado, en producción, listo, entregado, facturado, anulado) | "Módulo de Ventas – Pedidos" |
| RF-38 | Dos vistas del mismo módulo: vista de ventas (facturado/entregado) y vista de pedidos abiertos | "Mismo módulo, diferentes vistas" |
| RF-39 | Consulta al módulo `pricing` al cotizar; bloqueo del precio mientras quede asignado, salvo re-autorización | "Matriz de precios" |
| RF-40 | **Factura propia** con numeración correlativa por local y año; descuento del stock del local al emitir la factura | "Facturación propia" |
| RF-41 | **Nota de entrega** con los ítems físicos entregados; imprime desde módulo `documents` | "Gestión de documentos (nota de entrega)" |
| RF-42 | Cobro multi-moneda: monto en USD y Bs. registrado con tipo de cambio aplicado y referencia de tipo de pago (efectivo, punto, transferencia, divisa) | "Multi-moneda" |
| RF-43 | Anulación con reversa de stock y trámite de bitácora (justificación obligatoria) | Gaps operacionales |

### 8. pricing — Matriz de precios y fórmula

| ID | Requerimiento | Origen (crudo) |
| --- | --- | --- |
| RF-44 | **Matriz de precios**: precio base por combinación de producto / servicio / material / medida (p. ej. taza de 11 oz con vinil blanco, franela en S/M/L por m de tela) | "Tabla de muestra de servicios por producto, servicio, material y medida" |
| RF-45 | **Fórmula** aplicada al cotizar o exportar la matriz: `precio final = base × 1.30 (margen) × 1.16 (impuesto)`. Parametrizable si la tasa cambia | "Fórmula precio +30% +16%" |
| RF-46 | Historial de precios: cada cambio de la matriz conserva fecha, valor anterior y usuario, de modo que los cambios de precio no se sobrescriben a ciegas | Conversación de requerimientos |
| RF-47 | Vista de matriz para uso del vendedor y al administrador para mantenimiento | "Tabla de muestra..." |

### 9. hr — Trabajadores y personal

| ID | Requerimiento | Origen (crudo) |
| --- | --- | --- |
| RF-48 | CRUD de **trabajadores** con `cargo` (qué hace) y asignación multi-local (`trabajador_local`); cuando se les da login, se vincula a un `User` de identidad. **La nómina está diferida**: comisiones, liquidación y pagos van a fase posterior (RF-49–RF-51) | "Gestión de trabajadores" |
| RF-49 | *(diferido con la nómina)* Comisión definida por trabajador o rol (% sobre venta liquidada); se acumula cuando la venta cambia a estado `facturado`/`entregado` | "Contabilizar pagos por comisión" |
| RF-50 | *(diferido con la nómina)* Liquidación por periodo: acumulados por trabajador, adelantos descontados, pagados con modo y fecha; reporte mensual | "Contabilizar pagos por comisión" |
| RF-51 | *(diferido con la nómina)* Cada par (trabajador, venta) registra el % efectivo si la comisión varía por pedido especial | "Comisiones personalizadas" |

### 10. documents — Generador transversal

| ID | Requerimiento | Origen (crudo) |
| --- | --- | --- |
| RF-52 | **Generador de documentos** desde `sales`, `production`, `purchasing`, `reports`: factura propia, nota de entrega, orden de producción, planilla de transferencia, acta de desperdicio, comprobante de comisión *(diferido con la nómina)* | "Gestión de documentos (facturas, planillas...)" |
| RF-53 | Plantillas por documento editables por el admin (logos, datos fiscales, condiciones) y almacenamiento del PDF emitido | "Plantillas" |
| RF-54 | Numeración correlativa por (tipo de documento, local, año), reforzada a nivel de base de datos | "Facturación / numeración" |
| RF-55 | Repositorio de documentos emitidos con búsqueda por cliente, local, fecha, tipo | "Facturación / búsqueda" |

### 11. reports — Reportes y dashboard

| ID | Requerimiento | Origen (crudo) |
| --- | --- | --- |
| RF-56 | **Dashboard** por rol: ventas del día, pedidos en producción, stock crítico, comisiones por pagar *(diferido con la nómina)* | "Módulo de Dashboard" |
| RF-57 | Reportes: ventas por local/periodo, comparativa de proveedores, giro de inventario, desempeño de producción por máquina, comisiones *(diferido con la nómina)* | "Módulo de Reportes" |
| RF-58 | Exportar a CSV/PDF e imprimir desde browser | "Reportes exportables" |

## Total de RF

**58 requerimientos funcionales** en 11 módulos, trazables todos a la lista cruda (ningún RF se inventa sin respaldo; los conversacionales están marcados). En fase 1 se implementan **54**: RF-49, RF-50 y RF-51 (nómina y comisiones) quedan **diferidos** ([09 Decisiones diferidas y fases](09-decisiones-diferidas-y-fases.md)), y RF-12 (diseños) se administra externamente por el diseñador fuera del sistema.

---

## RNF — Requerimientos no funcionales

| ID | Requerimiento |
| --- | --- |
| RNF-01 | Web responsiva; el uso desde tablet en el piso de producción corre sobre la misma interfaz, no una app aparte |
| RNF-02 | Django 5+ y PostgreSQL 14+, desplegados en **un servidor central único**; los 3 locales se conectan por internet |
| RNF-03 | Autenticación con sesiones firmadas, contraseñas hasheadas (PBKDF2/Argon2), permisos verificados a nivel de servidor, no solo de UI |
| RNF-04 | **Toda** escritura en entidades de negocio (stock, venta, compra, producción, comisión) genera log auditable append-only |
| RNF-05 | Multi-moneda (USD + Bs.) con tipo de cambio editable por admin e histórico conservado para precisión contable |
| RNF-06 | Copias de seguridad PostgreSQL diarias automáticas; probabilidad de recuperación RPO ≤ 24 h |
| RNF-07 | Latencia operativa: pantallas de consulta y registro devuelven en ≤ 2 s con los 3 locales concentrando hasta 50 usuarios concurrentes |
| RNF-08 | Español neutro en UI; texto de mensajes de negocio en locale gestionado (i18n-ready), no strings hard-coded |

## Referencias

- [Glosario](referencias/glosario-del-negocio.md)
- [05 Flujos de proceso](05-flujos-de-proceso.md)