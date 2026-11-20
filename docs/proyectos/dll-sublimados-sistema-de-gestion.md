---
status: borrador
type: nota
tags:
  - proyecto
created: 2026-11-04
version: 0.2
---

# DLL Sublimados — sistema de gestión

Sistema integral para el negocio **DLL Sublimados** (sublimación, planchado y confección de prendas y otros objetos), distribuido en **3 locales**. Consta de un monolito modular Django + PostgreSQL (backend/API) y un frontend SPA en React + Vite + Tailwind CSS, con servidor central que conecta los 3 locales por internet.

## Estado

- Fase de **especificación**: requerimientos depurados, módulos, flujos y modelo de datos en construcción.
- La especificación está completa; el código va por detrás en varios puntos, con las divergencias detalladas en [12 Estado del código vs especificación](../12-estado-del-codigo-vs-especificacion.md).

## Documentación

- [00 Índice del sistema](../00-indice-del-sistema.md) — entrada a toda la especificación.
- [01 Resumen ejecutivo](../01-resumen-ejecutivo.md) — el negocio en un página y las 11 apps Django.
- [03 Requerimientos del sistema](../03-requerimientos-del-sistema.md) — los 58 RF y los 8 RNF.
- [04 Arquitectura del monolito modular](../04-arquitectura-del-monolito-modular.md) — cómo se organiza el código y cómo se despliega.
- [05 Flujos de proceso](../05-flujos-de-proceso.md) — los 6 flujos críticos.
- [06 Modelo de datos](../06-modelo-de-datos.md) — el modelo por esquema y el MER transversal.
- [07 Convenciones de base de datos](../07-convenciones-de-base-de-datos.md) — naming, tipos, índices y auditoría.
- [08 Estructura del frontend](../08-estructura-del-frontend.md) — la SPA y sus páginas por módulo.
- [09 Decisiones diferidas y fases](../09-decisiones-diferidas-y-fases.md) — lo que quedó fuera y el plan de fases.
- [10 Git Flow y normas del equipo](../10-git-flow-y-normas-del-equipo.md) — repositorio, ramas, comandos y equipos.
- [11 Normas de código y POO](../11-normas-de-codigo-y-poo.md) — PEP 8, docstrings, POO y entorno virtual.
- [12 Estado del código vs especificación](../12-estado-del-codigo-vs-especificacion.md) — el retrato del estado real del repositorio.
- [13 Instalación y entorno local](../13-instalacion-y-entorno-local.md) — entorno virtual, variables de entorno y estructura del repositorio.
- [14 Convenciones de commits](../14-convenciones-de-commits.md) — Conventional Commits, títulos, viñetas explicativas y revisión en PR.
- [Glosario del negocio](../referencias/glosario-del-negocio.md) — términos definidos (rollo, medición, sobrante, comisión…).

## Ficha rápida

| Aspecto | Valor |
| --- | --- |
| Negocio | DLL Sublimados (sublimación, planchado, confección) |
| Locales | 3 (principal: impresión y corte; otros: planchado, confección, diseño) |
| Stack | Django + PostgreSQL (API), React + Vite + Tailwind CSS (SPA), monolito modular |
| Módulos | 11 módulos de negocio en 12 apps Django: `core.identity`, `core.audit`, `catalog`, `inventory`, `purchasing`, `production`, `sales`, `pricing`, `hr`, `documents`, `reports`, más `core.common` como infraestructura compartida |
| Moneda | Multi-moneda USD / Bs., con tipo de cambio del día |
| Trazabilidad | Stock por local con consolidado global; lotes/rollos con medición, sobrante y desperdicio |
| Reglas | Toda escritura pasa por Pull Request; PEP 8 y docstrings obligatorios (ver [11 Normas de código y POO](../11-normas-de-codigo-y-poo.md)) |
| Licencia | Académica: uso exclusivo en la evaluación de Lenguajes de Programación III |

## Referencias

- [00 Índice del sistema](../00-indice-del-sistema.md)
- [Glosario](../referencias/glosario-del-negocio.md)
- [Convenciones de documentación](../convenciones-documentacion.md)
