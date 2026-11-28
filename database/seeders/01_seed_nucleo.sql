-- =============================================================================
-- 01_seed_nucleo.sql
-- Datos iniciales del núcleo y documentos: locales (L01, L02, L03),
-- tasa de cambio oficial de arranque, contadores correlativos por local y año,
-- y plantillas HTML base para documentos emitidos.
--
-- Nota sobre usuarios: el superadministrador y usuarios con contraseña PBKDF2
-- deben crearse vía Django (`python manage.py createsuperuser` o comando
-- `ensure_admin`). La tasa de cambio se enlaza automáticamente al primer
-- superusuario/admin existente.
--
-- Uso (después de `python manage.py migrate`):
--   psql "$DATABASE_URL" -f database/seeders/01_seed_nucleo.sql
--
-- Es idempotente: se puede volver a ejecutar sin duplicar nada.
-- =============================================================================

BEGIN;

-- -----------------------------------------------------------------------------
-- 1. Locales (RF-04).
-- -----------------------------------------------------------------------------
INSERT INTO nucleo.local (
    codigo, nombre, direccion, telefono, persona_contacto,
    creado_en, actualizado_en, activo
) VALUES
    ('L01', 'Local Principal', 'Sede Central - Impresión y Corte', '', '', now(), now(), true),
    ('L02', 'Local 2',         'Sucursal 2 - Planchado y Confección', '', '', now(), now(), true),
    ('L03', 'Local 3',         'Sucursal 3 - Diseño y Acabado', '', '', now(), now(), true)
ON CONFLICT (codigo) DO UPDATE
SET nombre = EXCLUDED.nombre,
    direccion = EXCLUDED.direccion,
    actualizado_en = now();

-- -----------------------------------------------------------------------------
-- 2. Tasa de cambio oficial de arranque (USD -> Bs.) (RNF-05).
--    Solo se inserta si aún no hay ninguna tasa activa registrada.
-- -----------------------------------------------------------------------------
INSERT INTO nucleo.tasa_cambio (
    fecha_vigencia, dolares_a_bs, registrado_por_id,
    creado_en, actualizado_en, activo
)
SELECT
    CURRENT_DATE,
    36.5000,
    (SELECT u.id FROM nucleo.usuario u WHERE u.is_superuser OR u.rol = 'admin' ORDER BY u.id LIMIT 1),
    now(),
    now(),
    true
WHERE NOT EXISTS (SELECT 1 FROM nucleo.tasa_cambio WHERE activo = true);

-- -----------------------------------------------------------------------------
-- 3. Contadores correlativos iniciales por (tipo_comprobante, local, año) (RF-54).
-- -----------------------------------------------------------------------------
INSERT INTO nucleo.contador_correlativo (
    tipo_comprobante, prefijo, numero_actual, local_id, anio,
    creado_en, actualizado_en, activo
)
SELECT
    v.tipo_comprobante,
    v.prefijo,
    0,
    l.id,
    EXTRACT(YEAR FROM CURRENT_DATE)::SMALLINT,
    now(),
    now(),
    true
FROM nucleo.local l
CROSS JOIN (VALUES
    ('factura',                'FAC'),
    ('nota_entrega',           'NE'),
    ('orden_produccion',       'OP'),
    ('presupuesto',            'PRE'),
    ('planilla_transferencia', 'TRA'),
    ('acta_desperdicio',       'DES'),
    ('comprobante_comision',   'COM')
) AS v (tipo_comprobante, prefijo)
WHERE l.codigo IN ('L01', 'L02', 'L03')
ON CONFLICT (tipo_comprobante, local_id, anio) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 4. Plantillas base HTML para generación de documentos (RF-53).
-- -----------------------------------------------------------------------------
INSERT INTO documentos.plantilla_documento (
    codigo, nombre, tipo, contenido_html, version,
    es_predeterminada, ruta_archivo, activo, creado_en, actualizado_en
) VALUES
    (
        'PLANT-FAC-BASE',
        'Factura Propia Base',
        'factura',
        '<!DOCTYPE html><html lang="es"><body><h1>Factura {{ correlativo }}</h1><p>Local: {{ local.nombre }} | Fecha: {{ fecha_emision }}</p><p>Cliente: {{ cliente.nombre }}</p><p>Total: {{ total }} {{ moneda }}</p></body></html>',
        '1.0',
        true,
        '',
        true,
        now(),
        now()
    ),
    (
        'PLANT-NE-BASE',
        'Nota de Entrega Base',
        'nota_entrega',
        '<!DOCTYPE html><html lang="es"><body><h1>Nota de Entrega {{ correlativo }}</h1><p>Local: {{ local.nombre }} | Fecha: {{ fecha_emision }}</p><p>Cliente: {{ cliente.nombre }}</p></body></html>',
        '1.0',
        true,
        '',
        true,
        now(),
        now()
    ),
    (
        'PLANT-PRE-BASE',
        'Presupuesto Comercial Base',
        'presupuesto',
        '<!DOCTYPE html><html lang="es"><body><h1>Presupuesto {{ correlativo }}</h1><p>Local: {{ local.nombre }} | Fecha: {{ fecha_emision }}</p><p>Cliente: {{ cliente.nombre }}</p><p>Total estimado: {{ total }} {{ moneda }}</p></body></html>',
        '1.0',
        true,
        '',
        true,
        now(),
        now()
    ),
    (
        'PLANT-OP-BASE',
        'Orden de Producción Base',
        'orden_produccion',
        '<!DOCTYPE html><html lang="es"><body><h1>Orden de Producción {{ correlativo }}</h1><p>Local origen: {{ local.nombre }} | Fecha: {{ fecha_emision }}</p><p>Variante: {{ variante }} | Cantidad: {{ cantidad }}</p></body></html>',
        '1.0',
        true,
        '',
        true,
        now(),
        now()
    )
ON CONFLICT (codigo) DO NOTHING;

COMMIT;

