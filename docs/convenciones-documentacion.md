---
status: activo
type: convenciones
tags:
  - documentacion
created: 2026-11-04
version: 0.2
---

# Convenciones de documentación

Reglas que sigue el asistente al crear o editar notas de este vault.
Léelas antes de generar documentación nueva.

## Estructura de carpetas

- `Documentación/` — especificación del sistema (requerimientos, arquitectura, flujos, modelo de datos).
- `Documentación/modelo-datos/` — un ERD por esquema. Los archivos se llaman `06.<n> <esquema>.md`.
- `Documentación/ddl/` — el SQL de un esquema por archivo. Los archivos se llaman `06b.<n> <esquema>.md`.
- `Proyectos/` — una nota por proyecto, enlazada desde su documento técnico.
- `Plantillas/` — plantillas reutilizables: `Documento técnico`, `Nota` y `Decisión`.
- `Referencias/` — notas de apoyo y conceptos sueltos.

## Frontmatter obligatorio

Todo documento nuevo lleva estos campos:

| Campo | Valores válidos | Cuándo |
| --- | --- | --- |
| `status` | `borrador`, `revisar`, `publicado`, `obsoleto` | siempre |
| `type` | `documento`, `nota`, `decision`, `convenciones` | siempre |
| `tags` | lista YAML de strings en minúsculas | siempre |
| `created` | `AAAA-MM-DD` | siempre |
| `version` | `0.1`, `0.2`… | solo documentos técnicos |

No inventes campos que no estén en esta tabla sin comentarlo antes.

## Estilo

- Un solo `H1` (`#`), que coincide con el nombre del fichero.
- Encabezados en modo oración: `## Cómo desplegar`, no `## CÓMO DESPLEGAR`.
- Frases cortas. Viñetas cuando haya más de tres elementos.
- Español neutro. La prosa va en español; el modelo de datos también (tablas y columnas); el resto del código (funciones, servicios, componentes de React), en inglés.
- Los diagramas se escriben en Mermaid dentro del bloque de la nota. No se versionan imágenes binarias: todo diagrama va en Mermaid, y la documentación es 100 % Markdown.

## Enlaces

- Entre notas del vault: wikilink `[[Nombre de la nota]]`.
- Con alias solo si el texto enlazado no coincide: `[[Nota|este texto]]`.
- A web: Markdown normal `[texto](https://…)`.
- Cada documento de `Documentación` debe enlazar al menos a una nota de `Referencias`.
- Todo documento de `Documentación` termina en una sección `## Referencias`.
- Las notas de `modelo-datos/` y `ddl/` incluyen además una sección `## Navegación` con el enlace a la nota anterior y a la siguiente.

## Tamaño de las notas

- Una nota, un tema. Si una nota pasa de ~180 líneas, se divide: la nota madre queda como índice y el detalle va a notas hijas enlazadas.
- Nada se duplica entre notas: si un contenido aparece en dos sitios, una nota lo enlaza.

## Edición de notas existentes

- Actualiza el campo `version` solo si el cambio altera el significado.
- Nunca reescribas el bloque `---` completo: usa ediciones puntuales sobre la
  clave de frontmatter o el encabezado concreto.
- Si `status` es `publicado`, no lo cambies sin que lo pidas.

## Antes de terminar

1. Frontmatter completo y válido.
2. Al menos un wikilink saliente.
3. Sin `status: publicado` salvo petición explícita.
4. Todos los wikilinks resuelven a una nota existente.
5. Ninguna nota supera los ~180 líneas.

## Sincronización con el repositorio

La documentación vive también en `docs/` del repositorio del proyecto, con los mismos
contenidos pero con wikilinks convertidos en enlaces Markdown relativos. El vault es la
fuente de verdad: cuando cambia una nota, hay que reflejar el cambio en el repositorio.
