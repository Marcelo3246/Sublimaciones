---
status: vigente
type: documento
tags:
  - divergencias
  - codigo
  - especificacion
  - trazabilidad
created: 2026-11-15
updated: 2026-11-25
version: 0.2
---

# 12 Estado del código vs especificación

Estado consolidado de alineación entre la especificación del vault ([03 Requerimientos del sistema](03-requerimientos-del-sistema.md), [06 Modelo de datos](06-modelo-de-datos.md), [06b Esquemas y DDL PostgreSQL](06b-esquemas-y-ddl-postgresql.md)), la implementación en `backend/` y `database/`, y el despliegue en producción sobre Neon (`falling-firefly-71986564`, branch `production`).

## Estado de la capa de Base de Datos (Completado)

Tras la consolidación de esquemas canónicos (`backend.common.pgschema`), los modelos de los 10 módulos con persistencia, los scripts DDL en `database/` y la documentación técnica están **100 % unificados** con Neon:

| Capa | Estado | Detalle |
| --- | --- | --- |
| **Infraestructura Django / Neon** | **Conforme** | Django 6.1 (`backend/config/settings.py`) + PostgreSQL en Neon (`DATABASE_URL` con PgBouncer para la app y `DATABASE_URL_UNPOOLED` para migraciones). |
| **Aislamiento por esquemas** | **Conforme** | 10 esquemas PostgreSQL (`nucleo`, `auditoria`, `catalogo`, `inventario`, `compras`, `produccion`, `ventas`, `precios`, `rrhh`, `documentos`) implementados con `Meta.db_table` calificado y `backend.common.pgschema`. `reports` no posee tablas. |
| **Tablas y migraciones en Neon** | **Conforme (47 dominio + 7 Django)** | Las 45 tablas de negocio + 2 M2M (`nucleo.usuario_groups`, `nucleo.usuario_user_permissions`) + 7 tablas Django en `public` están migradas en Neon (`makemigrations --check --dry-run` sin cambios). |
| **Constraints `CHECK` y `UNIQUE`** | **Conforme** | Todas las enumeraciones `TextChoices` de los 10 módulos tienen su `CheckConstraint` correspondiente en BD; reglas XOR y montos/cantidades positivas validadas por `CHECK`. |
| **Scripts SQL y Seeders** | **Conforme** | `database/01_nucleo.sql`..`10_documentos.sql` alineados con Django/Neon; seeders maestros (`01_seed_nucleo.sql`, `02_seed_catalogo_inventario.sql`, maestros de `03` y `04`) cargados en Neon `production`. |
| **Documentación de BD (`06*`, `06b*`, `07`)** | **Sincronizada** | ERDs (`06.1`–`06.11`) y DDLs (`06b.1`–`06b.11`) actualizados al diseño unificado (`activo`, `es_global`, `USD`/`VES`, rol embebido en `nucleo.usuario`). |

## Decisiones de diseño consolidadas

| Tema | Decisión unificada | Justificación |
| --- | --- | --- |
| **Roles y alcance multi-local** | `Usuario.rol` (`admin`, `gerente`, `operario`, `vendedor`) + `Usuario.local` + `es_global` + `PermissionsMixin` | Evita tablas redundantes (`nucleo.rol`, `usuario_rol`, `usuario_local`); la matriz granular de permisos vive en código (`permissions.py`). |
| **Booleanos y mixins** | `TimeStampedModel` (`creado_en`, `actualizado_en`) + `ActivoMixin` (`activo`), `es_global`, `es_principal`, `es_predeterminada` | Convención uniforme en español en todo el modelo de negocio (`is_superuser` reservado de Django). |
| **Moneda y estados** | Moneda `USD` \| `VES` y estados de negocio en MAYÚSCULA (salvo `Usuario.rol` y `documents` en minúscula) | Alineado entre `choices.py`, `CHECK` de PostgreSQL, scripts SQL y seeders. |
| **Alcance fase 1 (`rrhh` y `catalog`)** | Nómina/comisiones diferidas a fase 4; diseños digitales gestionados externamente | Conforme con [03 Requerimientos del sistema](03-requerimientos-del-sistema.md) (RF-12) y [09 Decisiones diferidas y fases](09-decisiones-diferidas-y-fases.md). |

## Pendientes fuera de la capa de Base de Datos

La base de datos está culminada y operativa para el arranque de los demás equipos:

| Área | Equipo responsable | Pendiente |
| --- | --- | --- |
| **Backend (API y Servicios)** | Grupo de Backend | Implementar lógica de negocio en `services.py`, `permissions.py`, serializers, views y endpoints `/api/v1/` de los 11 módulos. |
| **Frontend (SPA React)** | Grupo de Frontend | Conectar las 11 features de `frontend/src/features/` contra los endpoints reales de la API REST. |
| **Pruebas de integración** | Backend / Gestión | Ejecutar `pytest` completo contra PostgreSQL (local o branch de prueba en Neon) conforme avancen los servicios y endpoints. |

## Referencias
- [03 Requerimientos del sistema](03-requerimientos-del-sistema.md)
- [06 Modelo de datos](06-modelo-de-datos.md)
- [06b Esquemas y DDL PostgreSQL](06b-esquemas-y-ddl-postgresql.md)
- [07 Convenciones de base de datos](07-convenciones-de-base-de-datos.md)
- [09 Decisiones diferidas y fases](09-decisiones-diferidas-y-fases.md)
- [neon.md](neon.md)
