-- =============================================================================
-- 99_migrar_esquemas.sql
-- Script de transición: mueve las tablas existentes en Neon del esquema
-- public a sus esquemas canónicos, conservando todos los datos.
--
-- Solo afecta a las tablas de core/audit/documents que ya están aplicadas
-- en Neon. Las tablas de catalog/inventory/purchasing/production/sales/
-- pricing/hr se crean directamente en su esquema con la migración 0001.
--
-- IMPORTANTE: Ejecutar ANTES de aplicar las nuevas migraciones Django que
-- hacen AlterModelTable. Si Django ya migró, este script es innecesario.
--
-- Uso:
--   psql "$DATABASE_URL" -f database/99_migrar_esquemas.sql
-- =============================================================================

BEGIN;

-- =============================================================================
-- 1. Crear los esquemas de destino
-- =============================================================================
CREATE SCHEMA IF NOT EXISTS nucleo;
CREATE SCHEMA IF NOT EXISTS auditoria;
CREATE SCHEMA IF NOT EXISTS documentos;

-- =============================================================================
-- 2. Núcleo: locales, usuarios (+ m2m), tasa_cambio, contador_correlativo
-- =============================================================================

-- 2a. locales → nucleo.local
ALTER TABLE public.locales SET SCHEMA nucleo;
ALTER TABLE nucleo.locales RENAME TO local;

-- 2b. usuarios → nucleo.usuario (primero las tablas que dependen de ella)
-- m2m: auth_user_groups → nucleo.usuario_groups
ALTER TABLE public.usuarios_groups SET SCHEMA nucleo;
ALTER TABLE nucleo.usuarios_groups RENAME TO usuario_groups;

-- m2m: auth_user_permissions → nucleo.usuario_user_permissions
ALTER TABLE public.usuarios_user_permissions SET SCHEMA nucleo;
ALTER TABLE nucleo.usuarios_user_permissions RENAME TO usuario_user_permissions;

-- La tabla principal
ALTER TABLE public.usuarios SET SCHEMA nucleo;
ALTER TABLE nucleo.usuarios RENAME TO usuario;

-- 2c. core_tasa_cambio → nucleo.tasa_cambio
ALTER TABLE public.core_tasa_cambio SET SCHEMA nucleo;
ALTER TABLE nucleo.core_tasa_cambio RENAME TO tasa_cambio;

-- 2d. core_contador_correlativo → nucleo.contador_correlativo
ALTER TABLE public.core_contador_correlativo SET SCHEMA nucleo;
ALTER TABLE nucleo.core_contador_correlativo RENAME TO contador_correlativo;

-- =============================================================================
-- 3. Auditoría
-- =============================================================================
ALTER TABLE public.audit_bitacora_accion SET SCHEMA auditoria;
ALTER TABLE auditoria.audit_bitacora_accion RENAME TO bitacora_accion;

ALTER TABLE public.audit_bitacora_stock SET SCHEMA auditoria;
ALTER TABLE auditoria.audit_bitacora_stock RENAME TO bitacora_stock;

-- =============================================================================
-- 4. Documentos
-- =============================================================================
ALTER TABLE public.documents_plantilla SET SCHEMA documentos;
ALTER TABLE documentos.documents_plantilla RENAME TO plantilla_documento;

ALTER TABLE public.documents_documento SET SCHEMA documentos;
ALTER TABLE documentos.documents_documento RENAME TO documento;

-- =============================================================================
-- 5. Actualizar la tabla django_migrations para que Django reconozca las
--    migraciones de esquema como ya aplicadas (evita re-ejecutar
--    AlterModelTable sobre tablas que ya están en su esquema destino).
-- =============================================================================
-- Marcar las migraciones de esquema como aplicadas
INSERT INTO public.django_migrations (app, name, applied)
VALUES
    ('core',      '0003_alter_contadorcorrelativo_table_alter_local_table_and_more', now()),
    ('audit',     '0002_alter_bitacoraaccion_table_alter_bitacorastock_table',       now()),
    ('documents', '0002_alter_documento_table_alter_plantilladocumento_table',       now())
ON CONFLICT DO NOTHING;

COMMIT;

-- =============================================================================
-- 6. Verificación: lista las tablas por esquema
-- =============================================================================
SELECT schemaname, tablename
FROM pg_tables
WHERE schemaname IN ('nucleo', 'auditoria', 'documentos')
ORDER BY schemaname, tablename;

