-- =============================================================================
-- 04_seed_ventas_precios_rrhh.sql
-- Datos iniciales de ventas, precios y recursos humanos: clientes base,
-- parámetros de la fórmula comercial, matriz de precios inicial y fichas de
-- trabajadores asignados a los locales L01, L02 y L03.
--
-- Uso (requiere antes: `python manage.py migrate`,
-- `database/01_datos_iniciales.sql` y
-- `database/seeders/02_seed_catalogo_inventario.sql`):
--   psql -U postgres -d dll_sublimados -f database/seeders/04_seed_ventas_precios_rrhh.sql
--
-- El parámetro de fórmula exige un usuario que lo registre: se toma el primer
-- usuario con rol 'admin'. Si aún no existe ninguno (seeder de núcleo
-- pendiente), esa sección se omite con un aviso y el resto se carga igual;
-- basta volver a ejecutar el seeder después de crear el administrador.
--
-- Es idempotente: se puede volver a ejecutar sin duplicar nada.
-- =============================================================================

BEGIN;

-- -----------------------------------------------------------------------------
-- 1. Clientes base (RF-36): el genérico "Consumidor Final" (sin RIF) y dos
--    clientes corporativos de prueba.
-- -----------------------------------------------------------------------------
INSERT INTO ventas.cliente (nombre, telefono, correo, rif, activo, creado_en, actualizado_en)
SELECT v.nombre, v.telefono, v.correo, v.rif, true, now(), now()
FROM (VALUES
    ('Consumidor Final',                 '',              '',                          NULL),
    ('Club Deportivo Los Halcones C.A.', '0212-555-0101', 'compras@halcones.example',  'J-40123456-7'),
    ('Eventos y Promociones Andina C.A.','0274-555-0202', 'pedidos@andina.example',    'J-30987654-1')
) AS v (nombre, telefono, correo, rif)
WHERE NOT EXISTS (
    SELECT 1 FROM ventas.cliente c
    WHERE c.nombre = v.nombre AND c.rif IS NOT DISTINCT FROM v.rif
);

-- -----------------------------------------------------------------------------
-- 2. Parámetro vigente de la fórmula comercial (RF-45):
--    margen 1.30 (+30 %) e IVA 0.16 (16 %), sin fecha de fin.
-- -----------------------------------------------------------------------------
INSERT INTO precios.parametro_formula
    (porcentaje_margen, porcentaje_iva, fecha_desde, fecha_hasta, registrado_por_id,
     activo, creado_en, actualizado_en)
SELECT 1.3000, 0.1600, DATE '2026-01-01', NULL, u.id, true, now(), now()
FROM (SELECT id FROM nucleo.usuario WHERE rol = 'admin' ORDER BY id LIMIT 1) AS u
ON CONFLICT (fecha_desde) DO NOTHING;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM nucleo.usuario WHERE rol = 'admin') THEN
        RAISE NOTICE 'No hay usuario admin: se omitió precios.parametro_formula. '
                     'Ejecute de nuevo este seeder tras crear el administrador.';
    END IF;
END $$;

-- -----------------------------------------------------------------------------
-- 3. Servicio de sublimación por metro (necesario para la matriz).
-- -----------------------------------------------------------------------------
INSERT INTO catalogo.servicio (nombre, descripcion, unidad_medida_id, activo, creado_en, actualizado_en)
SELECT 'Sublimación por metro',
       'Sublimación de tela por metro lineal (ancho 1.60 m).',
       (SELECT id FROM catalogo.unidad_medida WHERE codigo = 'm'),
       true, now(), now()
WHERE NOT EXISTS (SELECT 1 FROM catalogo.servicio WHERE nombre = 'Sublimación por metro');

-- -----------------------------------------------------------------------------
-- 4. Matriz de precios inicial (RF-44), en USD con margen 1.30 e IVA 0.16.
--    El precio final (base × margen × (1 + iva)) se calcula en servicios.
--    - Prendas estándar: franela, taza 11 oz (con su medida) y gorra.
--    - Servicio de sublimación por metro sobre microdurazno.
-- -----------------------------------------------------------------------------
INSERT INTO precios.item_matriz_precios
    (producto_id, variante_id, servicio_id, material_id, unidad_medida_id,
     medida_cantidad, unidad_medida_medida_id, precio_base, moneda,
     porcentaje_margen, porcentaje_iva, activo, creado_en, actualizado_en)
SELECT p.id, NULL, NULL, NULL, (SELECT id FROM catalogo.unidad_medida WHERE codigo = 'pza'),
       NULL, NULL, v.precio, 'USD', 1.3000, 0.1600, true, now(), now()
FROM (VALUES
    ('PROD-001', 8.00),   -- Franela deportiva sublimada
    ('PROD-003', 6.00)    -- Gorra trucker
) AS v (codigo, precio)
JOIN catalogo.producto p ON p.codigo = v.codigo
WHERE NOT EXISTS (
    SELECT 1 FROM precios.item_matriz_precios i
    WHERE i.producto_id = p.id AND i.material_id IS NULL AND i.medida_cantidad IS NULL
);

-- Taza 11 oz: la medida se guarda numérica (11) con su unidad (onza).
INSERT INTO catalogo.unidad_medida (codigo, nombre, permite_decimales, activo, creado_en, actualizado_en)
VALUES ('oz', 'Onza', true, true, now(), now())
ON CONFLICT (codigo) DO NOTHING;

INSERT INTO precios.item_matriz_precios
    (producto_id, variante_id, servicio_id, material_id, unidad_medida_id,
     medida_cantidad, unidad_medida_medida_id, precio_base, moneda,
     porcentaje_margen, porcentaje_iva, activo, creado_en, actualizado_en)
SELECT p.id, NULL, NULL, NULL, (SELECT id FROM catalogo.unidad_medida WHERE codigo = 'pza'),
       11, (SELECT id FROM catalogo.unidad_medida WHERE codigo = 'oz'),
       4.50, 'USD', 1.3000, 0.1600, true, now(), now()
FROM catalogo.producto p
WHERE p.codigo = 'PROD-002'
  AND NOT EXISTS (
      SELECT 1 FROM precios.item_matriz_precios i
      WHERE i.producto_id = p.id AND i.medida_cantidad = 11
  );

INSERT INTO precios.item_matriz_precios
    (producto_id, variante_id, servicio_id, material_id, unidad_medida_id,
     medida_cantidad, unidad_medida_medida_id, precio_base, moneda,
     porcentaje_margen, porcentaje_iva, activo, creado_en, actualizado_en)
SELECT NULL, NULL, s.id, m.id, (SELECT id FROM catalogo.unidad_medida WHERE codigo = 'm'),
       NULL, NULL, 3.50, 'USD', 1.3000, 0.1600, true, now(), now()
FROM catalogo.servicio s
JOIN catalogo.material m ON m.codigo = 'MAT-001'
WHERE s.nombre = 'Sublimación por metro'
  AND NOT EXISTS (
      SELECT 1 FROM precios.item_matriz_precios i
      WHERE i.servicio_id = s.id AND i.material_id = m.id
  );

-- -----------------------------------------------------------------------------
-- 5. Fichas de trabajadores (RF-48) y su local principal (L01, L02, L03).
--    Cargos según la especialidad de cada local: L01 imprime, L02 plancha y
--    confecciona, L03 diseña; un vendedor por local.
-- -----------------------------------------------------------------------------
INSERT INTO rrhh.trabajador
    (nombre_completo, cargo, telefono, correo, fecha_ingreso, usuario_id,
     activo, creado_en, actualizado_en)
SELECT v.nombre, v.cargo, '', '', DATE '2026-01-05', NULL, true, now(), now()
FROM (VALUES
    ('Vendedor Sede Central',  'VENDEDOR'),
    ('Impresor Sede Central',  'IMPRESOR'),
    ('Vendedor Sucursal 2',    'VENDEDOR'),
    ('Planchador Sucursal 2',  'PLANCHADOR'),
    ('Confeccionador Sucursal 2', 'CONFECCIONADOR'),
    ('Vendedor Sucursal 3',    'VENDEDOR'),
    ('Diseñador Sucursal 3',   'DISENADOR')
) AS v (nombre, cargo)
WHERE NOT EXISTS (SELECT 1 FROM rrhh.trabajador t WHERE t.nombre_completo = v.nombre);

INSERT INTO rrhh.trabajador_local
    (trabajador_id, local_id, es_principal, activo, creado_en, actualizado_en)
SELECT t.id, l.id, true, true, now(), now()
FROM (VALUES
    ('Vendedor Sede Central',     'L01'),
    ('Impresor Sede Central',     'L01'),
    ('Vendedor Sucursal 2',       'L02'),
    ('Planchador Sucursal 2',     'L02'),
    ('Confeccionador Sucursal 2', 'L02'),
    ('Vendedor Sucursal 3',       'L03'),
    ('Diseñador Sucursal 3',      'L03')
) AS v (nombre, local_codigo)
JOIN rrhh.trabajador t ON t.nombre_completo = v.nombre
JOIN nucleo.local l ON l.codigo = v.local_codigo
ON CONFLICT (trabajador_id, local_id) DO NOTHING;

-- El diseñador también apoya en L01 (asignación secundaria, multi-local).
INSERT INTO rrhh.trabajador_local
    (trabajador_id, local_id, es_principal, activo, creado_en, actualizado_en)
SELECT t.id, l.id, false, true, now(), now()
FROM rrhh.trabajador t
JOIN nucleo.local l ON l.codigo = 'L01'
WHERE t.nombre_completo = 'Diseñador Sucursal 3'
ON CONFLICT (trabajador_id, local_id) DO NOTHING;

COMMIT;
