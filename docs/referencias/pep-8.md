---
status: borrador
type: nota
tags:
  - python
  - pep8
  - estilo
created: 2026-11-15
---

# PEP 8

Guía de estilo de Python (Python Enhancement Proposal 8). Es el estándar que el proyecto exige para todo el código fuente en Python.

## Reglas que aplican al proyecto

| Regla | Detalle |
| --- | --- |
| Indentación | 4 espacios, nunca tabuladores |
| Longitud de línea | Máximo 79 caracteres (100 aceptable en URLs o cadenas largas) |
| Imports | En orden: biblioteca estándar, terceros, proyecto. Separados por línea en blanco |
| Nombres | `snake_case` para funciones y variables, `PascalCase` para clases, `UPPER_CASE` para constantes |
| Classes | Una clase por módulo, docstring obligatorio |
| Funciones | Máximo 3 niveles de indentación; si se complica, se extrae a un helper |
| Líneas en blanco | 2 entre clases y funciones de nivel superior, 1 dentro de clases |
| Strings | Comillas dobles por defecto; f-strings para interpolación |
| Comentarios | Explican el **porqué**, no el qué. El **qué** va en el docstring |

## Excepciones del proyecto

- Los modelos de Django usan **español** en tablas y columnas (`lote`, `cantidad_actual`, `precio_unitario`); la lógica que no es modelo va en inglés (`consume_material()`, `reserve_stock()`). Convención completa en [07 Convenciones de base de datos](../07-convenciones-de-base-de-datos.md).
- Los componentes de React usan `PascalCase` y los hooks `useXxx`.

## Docstrings

Toda clase, método y función lleva docstring. Formato mínimo:

```python
def reserve_stock(order_line):
    """Reserva la cantidad de stock de una línea de pedido.

    Recibe:
        order_line: línea de pedido con producto, cantidad y local.

    Retorna:
        La reserva creada, o None si no hay saldo disponible.
    """
```

## Referencias

- [11 Normas de código y POO](../11-normas-de-codigo-y-poo.md)
- [07 Convenciones de base de datos](../07-convenciones-de-base-de-datos.md)
