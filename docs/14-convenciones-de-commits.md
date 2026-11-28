---
status: borrador
type: documento
tags:
  - git
  - commits
  - convenciones
  - flujo-de-trabajo
  - especificacion
created: 2026-11-15
version: 0.1
---

# 14 Convenciones de commits

Estándar de mensajes de commit para el repositorio de **DLL Sublimados**. Se basa en **Conventional Commits 1.0.0**, con tipo y ámbito en inglés, asunto en español en modo imperativo, y cuerpo detallado para documentar con precisión cada cambio realizado.

## Estructura obligatoria del mensaje

Todo commit en ramas de trabajo (`feature/*`, `hotfix/*`, `bugfix/*`) debe seguir esta estructura:

```text
<tipo>(<ámbito>): <título en imperativo, minúscula, sin punto final>

- <descripción detallada del cambio 1>
- <descripción detallada del cambio 2>
- <descripción detallada del cambio 3>

Refs: RF-XX / Closes: #YY
```

Si el commit contiene pocos cambios o un ajuste puntual, la lista de viñetas puede reemplazarse por uno o dos párrafos normales explicativos. La línea en blanco entre el título y el cuerpo es **obligatoria**.

## Tipos de commit

| Tipo | Propósito | Ejemplo |
| --- | --- | --- |
| `feat` | Nueva funcionalidad (RF) | `feat(catalog): agrega modelo de variantes con talla` |
| `fix` | Corrección de bug | `fix(inventory): corrige descuento de stock al anular un pedido` |
| `docs` | Solo documentación | `docs(db): documenta el esquema de la tabla de lotes` |
| `refactor` | Reestructuración de código sin alterar lógica | `refactor(sales): extrae el calculo de total a services.py` |
| `perf` | Mejora de rendimiento | `perf(reports): indexa historial de precios por material` |
| `test` | Incorporación o ajuste de pruebas | `test(pricing): cubre formula base * 1.30 * 1.16` |
| `style` | Formato y estilo sin impacto en lógica | `style(core.audit): aplica isort y black en serializers` |
| `build` | Dependencias, empaquetado o herramientas | `build(deps): fija django en 6.1 y anade psycopg2` |
| `ci` | Integración continua y workflows | `ci(tests): ejecuta pytest en cada pull request` |
| `chore` | Mantenimiento rutinario y configuración | `chore(gitignore): ignora frontend/node_modules` |
| `revert` | Reversión de un commit anterior | `revert(pricing): descarta parametrizacion por vigencia` |

## Ámbitos válidos (`scope`)

El ámbito delimita el módulo o subsistema modificado:

- **Backend (12 apps):** `core.common`, `core.identity`, `core.audit`, `catalog`, `inventory`, `purchasing`, `production`, `sales`, `pricing`, `hr`, `documents`, `reports`.
- **General / Infraestructura:** `frontend`, `docs`, `deps`, `config`.

## Las 8 reglas del mensaje

1. **Título conciso (≤ 72 caracteres):** Minúsculas, modo imperativo ("agrega", "corrige", "actualiza") y sin punto final.
2. **Línea en blanco separadora:** Siempre separar el título del cuerpo con un salto de línea.
3. **Cuerpo con desglose explícito:** Documentar qué cambió y por qué. Utilizar viñetas con guiones (`-`) para enumerar los cambios cuando sean varios, o párrafos continuos si son pocos. Texto envuelto a 72 caracteres.
4. **Un commit = una responsabilidad atómica:** No agrupar cambios disjuntos en un único commit ("hacer una sola cosa bien").
5. **Pie para trazabilidad:** Vincular al requerimiento o issue correspondiente (`Refs: RF-23`, `Closes: #42`).
6. **Reescribir antes de integrar:** En ramas locales de feature, usar `git commit --amend` o rebase interactivo para consolidar y limpiar mensajes antes de abrir el PR.
7. **Merges intactos:** Los commits automáticos de merge de Git Flow (`Merge branch '...' into ...`) no se modifican ni se someten a reescritura.
8. **Separar estilo de lógica:** Los formateos masivos (`style`) o de dependencias (`build`) deben ir en commits aislados de los cambios de negocio (`feat`/`fix`).

## Ejemplos del repositorio: buenos vs malos

| Estado | Mensaje | Motivo del veredicto |
| --- | --- | --- |
| ❌ | `repo listo con django y estructura lista` | Sin tipo, sin ámbito, no imperativo, impreciso y sin cuerpo. |
| ❌ | `venv` | Una sola palabra sin tipo, ámbito ni contexto de librerías. |
| ❌ | `repo listo para trabajar` | Subjetivo, vago y sin desglose de los archivos añadidos. |
| ✅ | `build(config): inicializa proyecto Django y estructura base`<br><br>`- genera settings y urls raiz`<br>`- define apps de negocio en INSTALLED_APPS`<br>`- agrega dependencias en requirements.txt` | Sigue Conventional Commits, ámbito claro y desglose detallado. |
| ✅ | `chore(venv): configura entorno virtual e instala dependencias`<br><br>`- crea venv con Python 3.12+`<br>`- instala Django y psycopg2`<br>`- anade venv/ a .gitignore` | Explica exactamente qué contiene el commit y el porqué. |
| ✅ | `feat(core.identity): anade modelos de usuario, rol y local`<br><br>`- implementa modelo Local con codigo unico`<br>`- anade modelo Rol con alcance global o por local`<br>`- extiende Usuario con soporte de autenticacion`<br><br>`Refs: RF-01, RF-02` | Título imperativo, lista de cambios y referencia al requerimiento. |

## Ejemplos por módulo

### Backend

```text
feat(inventory): agrega registro de sobrantes y desperdicio en rollo

- anade campos metros_sobrante y desperdicio_m2 en Partida
- valida que la suma no supere la cantidad inicial del lote
- registra la merma en la bitacora de auditoria

Refs: RF-21, RF-22
```

```text
fix(sales): recalcula saldo pendiente al registrar abono en caja

- descuenta el monto pagado del saldo de la factura
- actualiza el estado de la venta a 'pagado' cuando el saldo llega a 0

Refs: RF-35
```

### Frontend

```text
feat(frontend): implementa tabla interactiva con seleccion de local

- anade componente DataTable con ordenamiento y paginacion
- conecta SelectorLocal al store global de Zustand
- renderiza montos duales en USD y Bs en cada fila

Refs: RF-04, RNF-05
```

### Documentación y configuración

```text
docs(commits): formaliza convenciones de Conventional Commits

- documenta tipos, ambitos validos y estructura con viñetas
- agrega tabla de ejemplos correctos y correccion del historial
- integra paso de validacion de commits en el checklist de PR

Refs: RNF-08
```

## Checklist de revisión de commits en el Pull Request

El **Grupo de Gestión** verifica en cada PR:

1. ¿El título respeta el formato `<tipo>(<ámbito>): <título>`?
2. ¿El tipo pertenece a la lista de tipos válidos?
3. ¿El ámbito corresponde a una app de backend o a un subsistema oficial?
4. ¿El título está en español, imperativo, minúscula y sin punto?
5. ¿Existe una línea en blanco entre el título y el cuerpo?
6. ¿El cuerpo detalla los cambios (en viñetas para múltiples cambios o en párrafos limpios) y aporta el porqué?
7. ¿Se incluye la referencia al requerimiento (`Refs: RF-XX`) cuando aplica?

Si algún commit no cumple, el autor debe corregirlo con `git commit --amend` o rebase interactivo en su rama `feature/*` antes de la aprobación final.

## Referencias

- [10 Git Flow y normas del equipo](10-git-flow-y-normas-del-equipo.md)
- [11 Normas de código y POO](11-normas-de-codigo-y-poo.md)
- [00 Índice del sistema](00-indice-del-sistema.md)
- [03 Requerimientos del sistema](03-requerimientos-del-sistema.md)
- [Git Flow](referencias/git-flow.md)

