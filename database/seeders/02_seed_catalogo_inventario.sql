-- =============================================================================
-- 02_seed_catalogo_inventario.sql
-- Datos iniciales del catálogo maestro e inventario: unidades de medida,
-- tallas, categorías, subcategorías, materiales, productos y niveles
-- mínimos de stock por local (L01, L02, L03).
--
-- Uso (requiere antes: `python manage.py migrate` y
-- `database/01_datos_iniciales.sql` para los locales):
--   psql -U postgres -d dll_sublimados -f database/seeders/02_seed_catalogo_inventario.sql
--
-- Es idempotente: se puede volver a ejecutar sin duplicar nada.
-- =============================================================================

BEGIN;

-- -----------------------------------------------------------------------------
-- 1. Unidades de medida oficiales.
--    Los decimales se permiten en unidades de longitud/masa; el conteo de
--    rollos, piezas y unidades es entero.
-- -----------------------------------------------------------------------------
INSERT INTO catalogo.unidad_medida (codigo, nombre, permite_decimales, activo, creado_en, actualizado_en) VALUES
    ('m',     'Metro',      true,  true, now(), now()),
    ('cm',    'Centímetro', true,  true, now(), now()),
    ('kg',    'Kilo',       true,  true, now(), now()),
    ('rollo', 'Rollo',      false, true, now(), now()),
    ('pza',    'Pieza',     false, true, now(), now()),
    ('und',    'Unidad',    false, true, now(), now())
ON CONFLICT (codigo) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 2. Tallas adultas e infantiles (orden de presentación en catálogo).
-- -----------------------------------------------------------------------------
INSERT INTO catalogo.talla (codigo, nombre, orden, activo, creado_en, actualizado_en) VALUES
    ('XS',  'XS',   1,  true, now(), now()),
    ('S',   'S',    2,  true, now(), now()),
    ('M',   'M',    3,  true, now(), now()),
    ('L',   'L',    4,  true, now(), now()),
    ('XL',  'XL',   5,  true, now(), now()),
    ('XXL', 'XXL',  6,  true, now(), now()),
    ('4',   '4',    7,  true, now(), now()),
    ('6',   '6',    8,  true, now(), now()),
    ('8',   '8',    9,  true, now(), now()),
    ('10',  '10',   10, true, now(), now()),
    ('12',  '12',   11, true, now(), now()),
    ('14',  '14',   12, true, now(), now()),
    ('16',  '16',   13, true, now(), now())
ON CONFLICT (codigo) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 3. Categorías raíz: cuatro de materia prima y una de productos terminados.
-- -----------------------------------------------------------------------------
INSERT INTO catalogo.categoria (nombre, tipo, activo, creado_en, actualizado_en) VALUES
    ('Telas Textiles',        'MATERIAL', true, now(), now()),
    ('Tintas y Químicos',     'MATERIAL', true, now(), now()),
    ('Viniles',               'MATERIAL', true, now(), now()),
    ('Papel de Sublimación',  'MATERIAL', true, now(), now()),
    ('Confección Terminada',  'PRODUCTO', true, now(), now())
ON CONFLICT (nombre, tipo) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 4. Subcategorías de la línea de productos terminados.
-- -----------------------------------------------------------------------------
INSERT INTO catalogo.subcategoria (categoria_id, nombre, activo, creado_en, actualizado_en) VALUES
    ((SELECT id FROM catalogo.categoria WHERE nombre = 'Confección Terminada' AND tipo = 'PRODUCTO'),
     'Prendas Deportivas', true, now(), now()),
    ((SELECT id FROM catalogo.categoria WHERE nombre = 'Confección Terminada' AND tipo = 'PRODUCTO'),
     'Tazas',              true, now(), now()),
    ((SELECT id FROM catalogo.categoria WHERE nombre = 'Confección Terminada' AND tipo = 'PRODUCTO'),
     'Gorras',             true, now(), now())
ON CONFLICT (categoria_id, nombre) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 5. Catálogo inicial de materiales.
--    Los textiles y el vinil se miden por longitud (es_continuo);
--    las tintas y el papel se cuentan por unidad/pieza.
-- -----------------------------------------------------------------------------
INSERT INTO catalogo.material
    (codigo, nombre, categoria_id, unidad_medida_id, es_continuo, stock_minimo_global, activo, creado_en, actualizado_en)
VALUES
    ('MAT-001', 'Rollo Microdurazno Blanco 1.60m',
        (SELECT id FROM catalogo.categoria   WHERE nombre = 'Telas Textiles'),
        (SELECT id FROM catalogo.unidad_medida WHERE codigo = 'm'),
        true, NULL, true, now(), now()),
    ('MAT-002', 'Tinta Sublimación Cyan',
        (SELECT id FROM catalogo.categoria   WHERE nombre = 'Tintas y Químicos'),
        (SELECT id FROM catalogo.unidad_medida WHERE codigo = 'und'),
        false, NULL, true, now(), now()),
    ('MAT-003', 'Tinta Sublimación Magenta',
        (SELECT id FROM catalogo.categoria   WHERE nombre = 'Tintas y Químicos'),
        (SELECT id FROM catalogo.unidad_medida WHERE codigo = 'und'),
        false, NULL, true, now(), now()),
    ('MAT-004', 'Tinta Sublimación Yellow',
        (SELECT id FROM catalogo.categoria   WHERE nombre = 'Tintas y Químicos'),
        (SELECT id FROM catalogo.unidad_medida WHERE codigo = 'und'),
        false, NULL, true, now(), now()),
    ('MAT-005', 'Tinta Sublimación Black',
        (SELECT id FROM catalogo.categoria   WHERE nombre = 'Tintas y Químicos'),
        (SELECT id FROM catalogo.unidad_medida WHERE codigo = 'und'),
        false, NULL, true, now(), now()),
    ('MAT-006', 'Vinil Textil Poliuretano',
        (SELECT id FROM catalogo.categoria   WHERE nombre = 'Viniles'),
        (SELECT id FROM catalogo.unidad_medida WHERE codigo = 'm'),
        true, NULL, true, now(), now()),
    ('MAT-007', 'Papel Sublimación 100gr',
        (SELECT id FROM catalogo.categoria   WHERE nombre = 'Papel de Sublimación'),
        (SELECT id FROM catalogo.unidad_medida WHERE codigo = 'pza'),
        false, NULL, true, now(), now())
ON CONFLICT (codigo) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 6. Catálogo de productos terminados listos para venta.
-- -----------------------------------------------------------------------------
INSERT INTO catalogo.producto
    (codigo, nombre, descripcion, subcategoria_id, tipo, activo, creado_en, actualizado_en)
VALUES
    ('PROD-001', 'Franela Deportiva Cuello Redondo Sublimada',
        'Franela deportiva con cuello redondo, sublimada a full color.',
        (SELECT id FROM catalogo.subcategoria WHERE nombre = 'Prendas Deportivas'),
        'TERMINADO', true, now(), now()),
    ('PROD-002', 'Taza Blanca 11oz',
        'Taza cerámica blanca de 11 oz lista para sublimar.',
        (SELECT id FROM catalogo.subcategoria WHERE nombre = 'Tazas'),
        'TERMINADO', true, now(), now()),
    ('PROD-003', 'Gorra Trucker',
        'Gorra trucker con frontal sublimable y malla trasera.',
        (SELECT id FROM catalogo.subcategoria WHERE nombre = 'Gorras'),
        'TERMINADO', true, now(), now())
ON CONFLICT (codigo) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 7. Niveles mínimos de alerta por material en cada local (L01, L02, L03).
--    Alertas: 2 rollos de tela/vinil, 10 cartuchos de tinta, 20 hojas de papel.
-- -----------------------------------------------------------------------------
INSERT INTO inventario.nivel_minimo
    (local_id, producto_id, material_id, cantidad_minima_alerta, activo, creado_en, actualizado_en)
SELECT
    l.id,
    NULL,
    m.id,
    v.minimo,
    true,
    now(),
    now()
FROM nucleo.local l
CROSS JOIN (VALUES
    ('MAT-001', 2),
    ('MAT-002', 10),
    ('MAT-003', 10),
    ('MAT-004', 10),
    ('MAT-005', 10),
    ('MAT-006', 2),
    ('MAT-007', 20)
) AS v (codigo, minimo)
JOIN catalogo.material m ON m.codigo = v.codigo
WHERE l.codigo IN ('L01', 'L02', 'L03')
ON CONFLICT (local_id, material_id) WHERE material_id IS NOT NULL DO NOTHING;

COMMIT;
