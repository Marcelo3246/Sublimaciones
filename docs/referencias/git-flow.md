---
status: borrador
type: nota
tags:
  - git
  - git-flow
created: 2026-11-15
---

# Git Flow

Modelo de ramificación para desarrollo paralelo con integraciones periódicas. En este proyecto se usa una **variante**: la rama de integración (`develop`) y la rama de prueba integral (`testeo`) están separadas, y el paso de `develop` a `testeo` a `main` lo hace el Grupo de Gestión mediante Pull Request.

## Ramas del modelo original

| Rama | Propósito | Vida útil | Se crea desde | Se fusiona en |
| --- | --- | --- | --- | --- |
| `main` | Código en producción | Permanente | — | — |
| `develop` | Integración del desarrollo activo | Permanente | `main` | `main` |
| `feature/*` | Desarrollo de funcionalidades nuevas | Temporal | `develop` | `develop` |
| `release/*` | Preparación de una versión para producción | Temporal | `develop` | `main` + `develop` |
| `hotfix/*` | Corrección urgente en producción | Temporal | `main` | `main` + `develop` |

## Qué cambia en DLL Sublimados

- La rama `release/*` **no existe**: el papel de preparar y validar una entrega lo cumple la rama `testeo`, sobre la que se prueba el proyecto integrado antes de llegar a `main`.
- Se añade `testeo`, que es una copia de `main` y solo recibe código ya validado en `develop`.
- El paso `develop → testeo → main` no es un `merge` directo del equipo: lo ejecuta el Grupo de Gestión tras la prueba integral.

El detalle de ramas, comandos y diagramas está en [10 Git Flow y normas del equipo](../10-git-flow-y-normas-del-equipo.md).

## Reglas de equipo que acompañan al modelo

- Nadie fuera del Grupo de Gestión hace `commit` ni `push` directo a `main`, `testeo` o `develop`.
- Todo código entra por Pull Request.
- Antes de pedir el PR, la rama local se actualiza con `git pull origin develop` y los conflictos se resuelven en la máquina del desarrollador.

## Referencias

- [10 Git Flow y normas del equipo](../10-git-flow-y-normas-del-equipo.md)
- [01 Resumen ejecutivo](../01-resumen-ejecutivo.md)
