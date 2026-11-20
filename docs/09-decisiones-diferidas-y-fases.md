---
status: borrador
type: documento
tags:
  - decisiones
  - fases
  - roadmap
created: 2026-11-04
version: 0.2
---

# 09 Decisiones diferidas y fases

Qué quedó fuera deliberadamente de la primera versión, por qué y cómo se preparó el diseño para que el costo de incorporarlo luego sea mínimo. Complementa las decisiones de fase 1 listadas en [01 Resumen ejecutivo](01-resumen-ejecutivo.md).

## Decisiones diferidas

### 1. Facturación fiscal (SENIAT / asesoramiento legal) — **diferida**

- **Estado en fase 1**: solo **facturación propia** (`factura.tipo = 'propia'`) con numeración correlativa por local.
- **Motivo**: el cliente aclaró que el sistema dual propio/SENIAT requiere asesoramiento legal antes de definir los requerimientos (formatos, leyendas, requisitos de emisión).
- **Cómo quedó preparado el diseño**:
  - `factura` ya nace con el campo `tipo` reservado (`propia` | `fiscal` para el futuro).
  - El documento se emite a través de `documentos`, así que el cambio de formato legal afecta plantillas, no modelos.
  - La fórmula de precio ya separa margen e impuesto (`base × 1.30 × 1.16`), de manera que el impuesto ya está aislado para la factura fiscal.
  - Queda pendiente definir los requisitos fiscales exactos con el asesoramiento legal antes de armar los requerimientos específicos.

### 2. Subcategorías — **diseñadas, sin uso en fase 1**

- `catalogo.subcategoria` existe en el modelo (FK desde material, producto y servicio), pero la creación de subcategorías queda deshabilitada en la UI hasta que el negocio defina cómo clasificar.
- **Motivo**: el cliente lo consideró aún sin determinar; el diseño previo evita una migración dolorosa después.

### 3. Integraciones externas y BI avanzado — **fuera de alcance inicial**

- Pasarelas de pago online, APIs de courier o dashboards de BI no se incluyen en fase 1; los `reports` de [03 Requerimientos del sistema](03-requerimientos-del-sistema.md) cubren la necesidad de dirección.

### 4. Nómina y comisiones — **diferida**

- **Estado en fase 1**: solo el **catálogo de personal** — `trabajador` con `cargo` (qué hace) y `trabajador_local` (en qué locales opera, con sede principal). La trazabilidad queda cubierta: quién vendió (`pedido_venta.vendedor_trabajador_id`) y quién operó cada máquina (`operacion_maquina.operador_trabajador_id`).
- **Motivo**: el negocio aún no definió la mecánica de comisiones (porcentajes, base de cálculo, periodicidad de liquidación). Documentarla ahora obligaría a inventar reglas que luego habría que rehacer.
- **Qué va diferido**: configuración de comisión por trabajador o rol (RF-49), acumulación por venta, periodos de planilla, adelantos, liquidación (RF-50), pagos y el porcentaje especial por pedido (RF-51), más el comprobante de comisión en `documents` y las métricas de comisiones en dashboard/reportes (RF-56, RF-57).
- **Cómo quedó preparado el diseño**: las FK de operador y vendedor ya existen y apuntan a `rrhh.trabajador`; al activar la nómina se agregan las tablas `config_comision`, `periodo_planilla`, `comision`, `adelanto`, `liquidacion` y `pago_trabajador` al esquema `rrhh`, sin tocar las existentes. El flujo 5 de [05 Flujos de proceso](05-flujos-de-proceso.md) queda documentado como guía de diseño de esa fase.

## Fases sugeridas

| Fase | Alcance | Módulos activos |
| --- | --- | --- |
| **Fase 0** | Setup del repo, Docker, proyecto Django, ambientes, autenticación, base de locales | `core.identity`, `core.audit`, `core.common`, shell de la app |
| **Fase 1a** | Catálogo + inventario base: materiales, productos, servicios, UM/tallas, lotes y stock por local. Vistas de producto y de materia prima | `catalog`, `inventory` |
| **Fase 1b** | Compras: proveedores, órdenes, recepciones y comparador de precios | `purchasing` |
| **Fase 1c** | Producción multi-local: pasos enfrentados a `catalog` + inventario (consumo por medición, máquinas, desperdicio) | `production` |
| **Fase 1d** | Ventas: clientes, pedidos, facturación propia, nota de entrega, matriz de precios con la fórmula | `sales`, `pricing`, `documents` |
| **Fase 1e** | Personal: trabajadores con cargo y asignación por local; dashboard y reportes | `hr`, `reports` |
| **Fase 2** | Ajustes y adopción en los 3 locales, MVP operativo en producción | todas |
| **Fase 3** | Facturación fiscal SENIAT (condicionada al asesoramiento legal), subcategorías activadas, mejoras de BI | `documents`, `sales`, `reports` |
| **Fase 4** | Nómina y comisiones: configuración, acumulación por venta, liquidación y pagos | `hr`, `sales`, `documents`, `reports` |

## Riesgos y atenuaciones

| Riesgo | Impacto | Atenuación |
| --- | --- | --- |
| Caída de internet en un local | Las operaciones del local quedan sin sistema | Plan de contingencia offline (planillas en papel + ingreso posterior, documentado en la capacitación) |
| Submedición de consumo de rollo | Pérdida de trazabilidad del sobrante | Validación de mínimos aprovechables y registro de desperdicio; trazabilidad por lote ([06 Modelo de datos](06-modelo-de-datos.md)) |
| Tipo de cambio sin supervisión | Comparativa de proveedores y facturas en moneda equivocada | Solo admin edita `tasa_cambio`, con bitácora e histórico obligatorios |
| Órdenes de producción con rutas cruzadas entre locales (varios pasos y transferencias) | Retrasos en el pedido | El estado por paso expone los retrasos; flujo 4 en [05 Flujos de proceso](05-flujos-de-proceso.md) |

## Referencias

- [Glosario](referencias/glosario-del-negocio.md)
- [01 Resumen ejecutivo](01-resumen-ejecutivo.md)
- [03 Requerimientos del sistema](03-requerimientos-del-sistema.md)