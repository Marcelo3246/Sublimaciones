---
status: borrador
type: documento
tags:
  - poo
  - pep8
  - normativa
  - convenciones
  - especificacion
created: 2026-11-15
version: 0.1
---

# 11 Normas de código y POO

Las reglas que todo el código del proyecto debe cumplir, venga de qué equipo venga. Son de cumplimiento obligatorio y se revisan en el Pull Request.

## Paradigma obligatorio: POO

El proyecto se rige estrictamente por **Programación Orientada a Objetos**.

| Pilar | Qué exige | Ejemplo en el proyecto |
| --- | --- | --- |
| **Encapsulamiento** | Los datos sensibles están protegidos dentro de la clase y solo se acceden por su interfaz | Las contraseñas se guardan hasheadas en el usuario y nunca se exponen en las respuestas de la API |
| **Herencia y polimorfismo** | Se reutiliza código a través de clases base | `Persona` de la cual heredan `Usuario`, `Cliente` y `Proveedor` |
| **Abstracción** | Se modelan las entidades del mundo real (Venta, Producto, Insumo) en los modelos de Django | `models.py` describe la entidad; la regla de negocio vive en `services.py` |

Detalle conceptual en [Programación Orientada a Objetos](referencias/programacion-orientada-a-objetos.md). El estado real de la jerarquía `Persona` en el código está en [12 Estado del código vs especificación](12-estado-del-codigo-vs-especificacion.md).

## Estándares de código

### PEP 8

Todo el código en Python sigue el estándar de estilo **PEP 8**: indentación de 4 espacios, líneas de máximo 79 caracteres, imports ordenados por origen, `snake_case` para funciones y variables, `PascalCase` para clases. Resumen de las reglas que aplican al proyecto en [PEP 8](referencias/pep-8.md).

### Docstrings obligatorios

Todo método, clase o función debe contener comentarios técnicos (*docstrings*) explicando **qué hace, qué recibe y qué retorna**. La documentación de la API REST es la primera línea del docstring.

```python
def consume_material(batch, measured_uom):
    """Descuenta del lote la cantidad consumida por medición.

    Recibe:
        batch: lote físico del que se consume.
        measured_uom: cantidad y unidad de medida del consumo.

    Retorna:
        El movimiento de stock generado por el consumo.
    """
```

### Sin variables globales innecesarias

Está prohibido el uso de variables globales innecesarias; todo debe estar encapsulado en sus respectivas clases. Las constantes compartidas (por ejemplo, el tipo de cambio por defecto) viven en la configuración del proyecto, no en el ámbito de un módulo.

### Nada de lógica de negocio en serializers ni en vistas

La regla de negocio reside en la **capa de servicios** (`services.py`). El serializador traduce, la vista despacha. Es la regla 6 de la arquitectura y el motivo de que el frontend pueda ser reemplazado sin tocar el backend.

## Convenciones de nombres

| Contexto | Regla | Ejemplos |
| --- | --- | --- |
| Modelo de datos | Español, `snake_case`, singular | `Lote`, `pedido_venta`, `cantidad_actual` |
| Lógica de código | Inglés | `consume_material()`, `reserve_stock()`, `quote_price()` |
| Componentes React | `PascalCase` | `<PriceMatrix />`, `<DataTable />` |
| Hooks React | `useXxx` | `useAuth`, `useLocalActivo` |
| Funciones de servicio | Verbo en snake_case, inglés | `reserve_stock()`, `receive_transfer()` |
| Commits | Conventional Commits con desglose | Ver [14 Convenciones de commits](14-convenciones-de-commits.md) |

La convención completa de la base de datos está en [07 Convenciones de base de datos](07-convenciones-de-base-de-datos.md) y la del frontend en [08 Estructura del frontend](08-estructura-del-frontend.md).

## Entorno virtual

Para no saturar el Python global y asegurar que todos los equipos usen las mismas versiones de las librerías, el uso del entorno virtual (`venv`) es **obligatorio**.

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
.\venv\Scripts\Activate.ps1     # Windows (PowerShell)
pip install -r src/requirements.txt
```

> 💡 `venv/` está en `.gitignore`. Nunca se sube al repositorio; solo `src/requirements.txt`.

## Puesta en marcha

Los pasos para levantar el proyecto en una máquina local (entorno virtual, `.env`, migraciones y servidor) están en [13 Instalación y entorno local](13-instalacion-y-entorno-local.md).

## Cómo se revisan estas normas

El revisor del Pull Request (Grupo de Gestión) comprueba, en este orden:

1. ¿Hay docstrings en toda clase, método y función nueva?
2. ¿El código cumple PEP 8 y respeta la convención de nombres?
3. ¿Hay lógica de negocio fuera de la capa de servicios?
4. ¿Hay variables globales o estado compartido fuera de las clases?
5. ¿La rama viene de `develop` actualizada y sin conflictos?
6. ¿Los commits cumplen Conventional Commits con título y desglose en viñetas o párrafo en el cuerpo? (ver [14 Convenciones de commits](14-convenciones-de-commits.md)).
7. ¿Todo modelo Django implementa obligatoriamente `class Meta` con `db_table` explícito, `verbose_name` y `verbose_name_plural`? (ver [07 Convenciones de base de datos](07-convenciones-de-base-de-datos.md)).

Un PR que no pasa estas comprobaciones se rechaza de inmediato (ver [10 Git Flow y normas del equipo](10-git-flow-y-normas-del-equipo.md)).

## Referencias

- [PEP 8](referencias/pep-8.md)
- [Programación Orientada a Objetos](referencias/programacion-orientada-a-objetos.md)
- [10 Git Flow y normas del equipo](10-git-flow-y-normas-del-equipo.md)
- [14 Convenciones de commits](14-convenciones-de-commits.md)
- [07 Convenciones de base de datos](07-convenciones-de-base-de-datos.md)
- [08 Estructura del frontend](08-estructura-del-frontend.md)
- [04 Arquitectura del monolito modular](04-arquitectura-del-monolito-modular.md)
