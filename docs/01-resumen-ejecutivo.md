---
status: borrador
type: documento
tags:
  - resumen-ejecutivo
  - especificacion
created: 2026-11-04
version: 0.2
---

# 01 Resumen ejecutivo

Especificación de **DLL Sublimados**, sistema de gestión integral para un negocio de sublimación, planchado y confección de prendas y otros objetos, con 3 sucursales (locales) conectadas a un **servidor central**. Destinado al dueño del negocio y al equipo de desarrollo que implementará el sistema con **Django + PostgreSQL** en el backend y **React + Vite + Tailwind CSS** en el frontend.

## Problema que resuelve

Hoy los 3 locales operan con gestión manual y desalineada: no hay control trazable de materia prima ni de stock entre sedes, la producción cruza locales sin registro formal (impresión y corte en el principal; planchado, confección y diseño en los otros), no existe comparación de precios entre proveedores, comisiones de trabajadores ni historial auditable de quién alteró qué. Se necesita un único sistema que estandarice estas operaciones y permita escalar la operación a otros locales sin duplicar procesos.

## Solución propuesta

Un **monolito modular** (véase [Monolito modular](referencias/monolito-modular.md)): un backend Django con PostgreSQL en un servidor central al que se conectan los 3 locales por internet, más un **frontend SPA en React (Vite + Tailwind CSS)** que consume la API REST en JSON. El backend se organiza en 11 módulos de negocio con bordes explícitos, de modo que la migración futura de un módulo a microservicios sea simple si el negocio crece.

> [!info] Magnitud
> La lista cruda de requerimientos iniciales tenía ~19 puntos con redundancias (panel de admin y bitácoras duplicadas, documentos vs. facturación, RRHH partido). La depuración los consolidó en **11 módulos**, cubiertos por **58 requerimientos funcionales** y **8 no funcionales**. Detalle en [03 Requerimientos del sistema](03-requerimientos-del-sistema.md).

## Módulos del sistema

| # | Módulo (app Django) | Responsabilidad central |
| --- | --- | --- |
| 1 | `identity` | Login/registro, usuarios, roles mixtos (por local o globales), locales, perfil del usuario |
| 2 | `audit` | Bitácora de acciones de usuario + bitácora de movimientos de stock + panel de administración |
| 3 | `catalog` | Materias primas, productos, servicios, categorías/subcategorías, UM/tallas, formatos de material |
| 4 | `inventory` | Stock por local, salidas/entradas/ajustes, transferencias entre locales, estados del material |
| 5 | `purchasing` | Proveedores, órdenes y recepción de compras, facturas de compra, comparador de precios |
| 6 | `production` | Órdenes de producción, ruta multi-local, consumo de material por medición, operaciones por máquina |
| 7 | `sales` | Clientes, pedidos, notas de entrega, facturación propia, multi-moneda |
| 8 | `pricing` | Matriz de precios producto/servicio/material/medida, fórmula `base × 1.30 × 1.16` |
| 9 | `hr` | Trabajadores (cargo, locales, login); *nómina y comisiones diferidas* ([09 Decisiones diferidas y fases](09-decisiones-diferidas-y-fases.md)) |
| 10 | `documents` | Generador de documentos transversales: facturas, notas de entrega, planillas, orden interna |
| 11 | `reports` | Reportes por local y KPIs para el panel de administración (dashboard) |

## Decisiones clave

| Decisión | Alternativa descartada | Motivo |
| --- | --- | --- |
| Monolito modular Django + PostgreSQL | Microservicios desde el día 1 | Equipo pequeño, dominio aún evolucionando; se mantiene la puerta abierta a extraer módulos |
| Servidor central único, 3 locales conectados por internet | BD local por sucursal + réplica | Simplicidad operativa: evita sincronizar datos entre locales |
| Usuarios mixtos: por local y globales | Todo el mundo ve todo | Protege el stock del local: los operarios solo ven su local |
| Materias primas en entradas con **trazabilidad por lote/rollo** (medición, sobrante, desperdicio) para formatos medibles; con lotes opcionales para otros formatos | Solo rollos, solo unidades | El negocio consume tela/vinil por medida, pero también vende tazas/franelas por unidad |
| Fórmula de precio: `base × 1.30` (margen) `× 1.16` (impuesto) | Margen aplicado sobre el base ya impuesto | Orden correcto acordado con el cliente |
| Facturación propia en fase 1, SENIAT **diferido** hasta asesoramiento legal | Fiscal dual ahora | El modelo se dejar listo con punto de extensión tipo `documento` |
| Visibilidad del stock entre locales | Stock oculto por local | El local principal necesita ver las otras sedes para abastecer |

## Alcance de la fase 1

Incluye los 11 módulos arriba descritos con sus flujos principales ([05 Flujos de proceso](05-flujos-de-proceso.md)). **Fuera de fase 1**: facturación fiscal SENIAT (espera asesoría legal), subcategorías aún sin uso (diseñadas como campo opcional), integración con pasarelas de pago online y BI avanzado. Detalle y cronograma en [09 Decisiones diferidas y fases](09-decisiones-diferidas-y-fases.md).

## Referencias

- [Monolito modular](referencias/monolito-modular.md)
- [Glosario](referencias/glosario-del-negocio.md)