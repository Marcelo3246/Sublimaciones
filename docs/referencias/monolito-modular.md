---
status: borrador
type: nota
tags:
  - arquitectura
  - django
created: 2026-11-04
---

# Monolito modular

Patrón arquitectónico elegido para el sistema cuando se discutieron los requerimientos: una sola aplicación Django con PostgreSQL, organizada como módulos de negocio con fronteras explícitas.

## La idea

- Un solo proceso desplegado, una sola base de datos.
- Dentro del código, cada dominio de negocio (inventario, ventas, producción…) vive en su propia `app` Django.
- Los límites entre módulos se tratan como si fueran servicios independientes: hoy evita el acoplamiento, mañana permite extraer un módulo a un microservicio sin rediseñar.

## Reglas mínimas para que sea realmente "modular"

1. Cada módulo expone una **capa de servicios** (`services.py`). Otros módulos llaman a esas funciones, nunca directo a los modelos ajenos.
2. Las llaves foráneas que cruzan módulos solo se crean si el acoplamiento es natural (p. ej. una venta referencia un cliente). Si no, se guarda solo el `id` sin FK.
3. Cada módulo tiene su propio `models.py`, `serializers` y `permissions`; nada de "un models.py gigante".
4. Los mensajes dominio-a-dominio pasan por funciones, no por tablas compartidas ocultas.

## Cuándo conviene

- Equipo pequeño, dominio que evoluciona rápido.
- No hay aún necesidad real de escalar por servicios separados.
- Se quiere caminar después hacia microservicios sin reescribir todo.

## Referencias

- [04 Arquitectura del monolito modular](../04-arquitectura-del-monolito-modular.md)
- [Glosario](glosario-del-negocio.md)