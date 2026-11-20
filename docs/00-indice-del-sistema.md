---
status: borrador
type: documento
tags:
  - indice
  - especificacion
created: 2026-11-04
version: 0.4
---

# 00 Índice del sistema

Punto de entrada a la especificación de **DLL Sublimados**: sistema de gestión para un negocio de sublimación, planchado y confección distribuido en 3 locales. La nota de proyecto está en [DLL Sublimados — sistema de gestión](proyectos/dll-sublimados-sistema-de-gestion.md).

## Qué hay en el vault

### Especificación del sistema

| Nota | Contenido |
| --- | --- |
| [01 Resumen ejecutivo](01-resumen-ejecutivo.md) | Visión general: negocio, decisiones clave, los 11 módulos y alcance de la fase 1. |
| [02 Descripción del negocio y locales](02-descripcion-del-negocio-y-locales.md) | Cómo opera cada local, qué fluye entre ellos y qué roles de usuario existen. |
| [03 Requerimientos del sistema](03-requerimientos-del-sistema.md) | Requerimientos funcionales (RF-01–RF-58) y no funcionales (RNF-01–RNF-08), trazados a la lista original. |
| [04 Arquitectura del monolito modular](04-arquitectura-del-monolito-modular.md) | Backend (apps Django), frontend (React/Vite/Tailwind), servidor central y reglas de comunicación. |
| [05 Flujos de proceso](05-flujos-de-proceso.md) | 6 flujos críticos en Mermaid con pasos numerados, incluida la máquina de estados del pedido. |
| [06 Modelo de datos](06-modelo-de-datos.md) | Índice del modelo, convenciones de lectura y MER transversal. El detalle por esquema está en [06.1 nucleo](modelo-datos/06.1-nucleo.md) y siguientes. |
| [06b Esquemas y DDL PostgreSQL](06b-esquemas-y-ddl-postgresql.md) | Índice del DDL. El SQL de cada esquema está en [06b.1 nucleo](ddl/06b.1-nucleo.md) y siguientes. |
| [07 Convenciones de base de datos](07-convenciones-de-base-de-datos.md) | Esquema por módulo, naming en español, tipos, borrado lógico, índices y auditoría. |
| [08 Estructura del frontend](08-estructura-del-frontend.md) | Organización de la SPA React + Vite + Tailwind: features, páginas por módulo, componentes UI. |
| [09 Decisiones diferidas y fases](09-decisiones-diferidas-y-fases.md) | Qué quedó fuera por ahora (SENIAT, subcategorías), riesgos y el plan de fases. |

### Normas del proyecto

| Nota | Contenido |
| --- | --- |
| [10 Git Flow y normas del equipo](10-git-flow-y-normas-del-equipo.md) | Políticas de repositorio, ramas (`main`, `testeo`, `develop`, `feature/*`, `hotfix/*`), comandos, equipos y responsabilidades. |
| [11 Normas de código y POO](11-normas-de-codigo-y-poo.md) | PEP 8, docstrings obligatorios, encapsulamiento, jerarquía de clases y entorno virtual. |
| [12 Estado del código vs especificación](12-estado-del-codigo-vs-especificacion.md) | Qué de la especificación está implementado, qué falta y en qué dirección se resuelve cada diferencia. |
| [13 Instalación y entorno local](13-instalacion-y-entorno-local.md) | Requisitos, entorno virtual, variables de entorno, comandos y estructura del repositorio. |
| [14 Convenciones de commits](14-convenciones-de-commits.md) | Estándar Conventional Commits, tipos, ámbitos, desglose con viñetas y checklist para PRs. |

### Modelo de datos por esquema

| # | Esquema | ERD | DDL |
| --- | --- | --- | --- |
| 1 | `nucleo` | [06.1 nucleo](modelo-datos/06.1-nucleo.md) | [06b.1 nucleo](ddl/06b.1-nucleo.md) |
| 2 | `auditoria` | [06.2 auditoria](modelo-datos/06.2-auditoria.md) | [06b.2 auditoria](ddl/06b.2-auditoria.md) |
| 3 | `catalogo` | [06.3 catalogo](modelo-datos/06.3-catalogo.md) | [06b.3 catalogo](ddl/06b.3-catalogo.md) |
| 4 | `inventario` | [06.4 inventario](modelo-datos/06.4-inventario.md) | [06b.4 inventario](ddl/06b.4-inventario.md) |
| 5 | `compras` | [06.5 compras](modelo-datos/06.5-compras.md) | [06b.5 compras](ddl/06b.5-compras.md) |
| 6 | `produccion` | [06.6 produccion](modelo-datos/06.6-produccion.md) | [06b.6 produccion](ddl/06b.6-produccion.md) |
| 7 | `ventas` | [06.7 ventas](modelo-datos/06.7-ventas.md) | [06b.7 ventas](ddl/06b.7-ventas.md) |
| 8 | `precios` | [06.8 precios](modelo-datos/06.8-precios.md) | [06b.8 precios](ddl/06b.8-precios.md) |
| 9 | `rrhh` | [06.9 rrhh](modelo-datos/06.9-rrhh.md) | [06b.9 rrhh](ddl/06b.9-rrhh.md) |
| 10 | `documentos` | [06.10 documentos](modelo-datos/06.10-documentos.md) | [06b.10 documentos](ddl/06b.10-documentos.md) |
| 11 | `reports` | [06.11 reports](modelo-datos/06.11-reports.md) | [06b.11 reports](ddl/06b.11-reports.md) |

## Notas de apoyo

- [Glosario del negocio](referencias/glosario-del-negocio.md) — definiciones: rollo, lote, medición, sobrante, comisión, matriz de precios.
- [Monolito modular](referencias/monolito-modular.md) — por qué este patrón y sus reglas mínimas.
- [Git Flow](referencias/git-flow.md) — el modelo de ramificación y su adaptación a este proyecto.
- [Programación Orientada a Objetos](referencias/programacion-orientada-a-objetos.md) — los cuatro pilares y su aplicación a Django.
- [PEP 8](referencias/pep-8.md) — el estándar de estilo de Python que el proyecto exige.

## Reglas de este vault

- [Convenciones de documentación](convenciones-documentacion.md) — frontmatter, estilo, enlaces y estructura de carpetas.
- `Plantillas/` — plantillas reutilizables: documento técnico, nota y decisión.

## Referencias

- [DLL Sublimados — sistema de gestión](proyectos/dll-sublimados-sistema-de-gestion.md)
- [Convenciones de documentación](convenciones-documentacion.md)
- [Glosario del negocio](referencias/glosario-del-negocio.md)
- [Monolito modular](referencias/monolito-modular.md)
