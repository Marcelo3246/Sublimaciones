-- =============================================================================
-- 01_datos_iniciales.sql
-- Datos base del sistema: locales iniciales.
--
-- Uso (después de `python manage.py migrate`):
--   psql -U postgres -d dll_sublimados -f database/01_datos_iniciales.sql
--
-- Es idempotente: se puede volver a ejecutar sin duplicar nada.
-- =============================================================================

BEGIN;

-- -----------------------------------------------------------------------------
-- 1. Locales (RF-04). El local principal imprime y corta; los otros dos planchan,
--    confeccionan y diseñan.
-- -----------------------------------------------------------------------------
INSERT INTO nucleo.local (codigo, nombre, direccion, telefono, persona_contacto, creado_en, actualizado_en, activo) VALUES
    ('L01', 'Local Principal', 'Sede Central - Impresión y Corte', '', '', now(), now(), true),
    ('L02', 'Local 2',         'Sucursal 2 - Planchado y Confección', '', '', now(), now(), true),
    ('L03', 'Local 3',         'Sucursal 3 - Diseño y Acabado', '', '', now(), now(), true)
ON CONFLICT (codigo) DO UPDATE
SET nombre = EXCLUDED.nombre,
    direccion = EXCLUDED.direccion,
    actualizado_en = now();

COMMIT;
