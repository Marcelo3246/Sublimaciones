-- =============================================================================
-- 03_seed_compras_produccion.sql
-- Datos iniciales de compras y producción: empresas/proveedores de insumos,
-- parque de máquinas por local (L01, L02, L03), una variante demo del
-- catálogo, órdenes de compra de prueba y una orden de producción piloto
-- con ruta multi-local L01 -> L02 (RF-31).
--
-- Uso (requiere antes: `python manage.py migrate`, los scripts
-- 01_datos_iniciales.sql y seeders/02_seed_catalogo_inventario.sql):
--   psql -U postgres -d dll_sublimados -f database/seeders/03_seed_compras_produccion.sql
--
-- Es idempotente: se puede volver a ejecutar sin duplicar nada.
-- Nota: la variante demo pertenece al catálogo (Gaby); se inserta aquí solo
-- porque la orden de producción piloto exige una variante y el seeder del
-- catálogo no incluye variantes.
-- =============================================================================

BEGIN;

-- -----------------------------------------------------------------------------
-- 1. Empresas proveedoras de insumos.
-- -----------------------------------------------------------------------------
INSERT INTO compras.empresa (nombre, rif, direccion, telefono, correo, activo, creado_en, actualizado_en) VALUES
    ('Distribuidora Textil del Lago, C.A.', 'J-30123456-7', 'Av. 5 de Julio, Maracaibo', '0261-5550101', 'ventas@textildellago.com.ve', true, now(), now()),
    ('Insumos Gráficos Caracas, C.A.',      'J-30654321-0', 'Av. Universidad, Caracas',  '0212-5550202', 'contacto@graficoscaracas.com.ve', true, now(), now()),
    ('Importadora Plóter Express, C.A.',    'J-29987654-3', 'Zona Industrial La Yaguara, Caracas', '0212-5550303', 'soporte@ploterexpress.com.ve', true, now(), now())
ON CONFLICT (rif) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 2. Proveedores (puntos de contacto; el comparador RF-28 usa varios
--    proveedores sobre los mismos materiales).
-- -----------------------------------------------------------------------------
INSERT INTO compras.proveedor
    (empresa_id, persona_contacto, telefono, correo, moneda_predeterminada, condiciones_pago, calificacion, activo, creado_en, actualizado_en)
SELECT e.id, v.persona_contacto, v.telefono, v.correo, v.moneda, v.condiciones, v.calif, true, now(), now()
FROM compras.empresa e
JOIN (VALUES
    ('Distribuidora Textil del Lago, C.A.', 'María González',   '0414-5550111', 'maria.gonzalez@textildellago.com.ve',   'USD', 'Crédito a 30 días', 5),
    ('Distribuidora Textil del Lago, C.A.', 'José Ramírez',     '0424-5550112', 'jose.ramirez@textildellago.com.ve',     'USD', 'Contado',           4),
    ('Insumos Gráficos Caracas, C.A.',      'Carlos Pérez',     '0412-5550221', 'carlos.perez@graficoscaracas.com.ve',   'USD', 'Crédito a 15 días', 4),
    ('Importadora Plóter Express, C.A.',    'Laura Rodríguez',  '0416-5550331', 'laura.rodriguez@ploterexpress.com.ve',  'USD', 'Contado',           5)
) AS v (empresa, persona_contacto, telefono, correo, moneda, condiciones, calif)
    ON v.empresa = e.nombre
WHERE NOT EXISTS (
    SELECT 1 FROM compras.proveedor p
    WHERE p.empresa_id = e.id AND p.persona_contacto = v.persona_contacto
);

-- -----------------------------------------------------------------------------
-- 3. Parque de máquinas por local.
-- -----------------------------------------------------------------------------
INSERT INTO produccion.maquina (codigo, nombre, local_id, tipo, estado, horas_operativas, activo, creado_en, actualizado_en) VALUES
    ('MQ-L01-001', 'Plóter de Sublimación Mimaki/Epson 1.60m', (SELECT id FROM nucleo.local WHERE codigo = 'L01'), 'IMPRESORA',   'OPERATIVA', 0, true, now(), now()),
    ('MQ-L01-002', 'Cortadora Láser Textil',                   (SELECT id FROM nucleo.local WHERE codigo = 'L01'), 'CORTADORA',   'OPERATIVA', 0, true, now(), now()),
    ('MQ-L02-001', 'Plancha Térmica Industrial 80x100cm',      (SELECT id FROM nucleo.local WHERE codigo = 'L02'), 'PLANCHA',     'OPERATIVA', 0, true, now(), now()),
    ('MQ-L02-002', 'Máquina de Coser Overlock 5 Hilos',        (SELECT id FROM nucleo.local WHERE codigo = 'L02'), 'OTRO',        'OPERATIVA', 0, true, now(), now()),
    ('MQ-L02-003', 'Máquina de Coser Recta',                   (SELECT id FROM nucleo.local WHERE codigo = 'L02'), 'OTRO',        'OPERATIVA', 0, true, now(), now()),
    ('MQ-L03-001', 'Estampadora Combo 8 en 1 (Gorras/Tazas)',  (SELECT id FROM nucleo.local WHERE codigo = 'L03'), 'OTRO',        'OPERATIVA', 0, true, now(), now()),
    ('MQ-L03-002', 'Plancha de Transfer Manual',               (SELECT id FROM nucleo.local WHERE codigo = 'L03'), 'PLANCHA',     'OPERATIVA', 0, true, now(), now())
ON CONFLICT (codigo) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 4. Variante demo de la franela (talla M) para la orden piloto.
-- -----------------------------------------------------------------------------
INSERT INTO catalogo.variante_producto (producto_id, talla_id, color, sku, codigo_barras, activo, creado_en, actualizado_en)
SELECT p.id, t.id, 'Blanco', 'FRANELA-M-BLANCO', '', true, now(), now()
FROM catalogo.producto p
JOIN catalogo.talla t ON t.codigo = 'M'
WHERE p.codigo = 'PROD-001'
ON CONFLICT (sku) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 5. Órdenes de compra de prueba (RF-26): una enviada a L01 con telas y
--    otra en borrador con papel de sublimación.
-- -----------------------------------------------------------------------------
INSERT INTO compras.orden_compra (numero_orden, proveedor_id, local_id, estado, total, moneda, fecha_emision, activo, creado_en, actualizado_en)
SELECT 'OC-0001', p.id, l.id, 'ENVIADA', 199.00, 'USD', CURRENT_DATE, true, now(), now()
FROM compras.proveedor p
JOIN compras.empresa e ON e.id = p.empresa_id AND e.rif = 'J-30123456-7'
JOIN nucleo.local l ON l.codigo = 'L01'
WHERE p.persona_contacto = 'María González'
ON CONFLICT (numero_orden) DO NOTHING;

INSERT INTO compras.orden_compra (numero_orden, proveedor_id, local_id, estado, total, moneda, fecha_emision, activo, creado_en, actualizado_en)
SELECT 'OC-0002', p.id, l.id, 'BORRADOR', 35.00, 'USD', CURRENT_DATE, true, now(), now()
FROM compras.proveedor p
JOIN compras.empresa e ON e.id = p.empresa_id AND e.rif = 'J-30654321-0'
JOIN nucleo.local l ON l.codigo = 'L01'
WHERE p.persona_contacto = 'Carlos Pérez'
ON CONFLICT (numero_orden) DO NOTHING;

-- Líneas de la OC-0001: 5 m de tela y 3 m de vinil
INSERT INTO compras.linea_orden_compra
    (orden_compra_id, material_id, unidad_medida_id, cantidad_solicitada, cantidad_recibida, precio_unitario, moneda, activo, creado_en, actualizado_en)
SELECT oc.id, m.id, um.id, v.cant, 0, v.precio, 'USD', true, now(), now()
FROM compras.orden_compra oc
CROSS JOIN (VALUES
    ('MAT-001', 5.0000, 45.00),
    ('MAT-006', 3.0000, 28.00)
) AS v (cod_material, cant, precio)
JOIN catalogo.material m ON m.codigo = v.cod_material
JOIN catalogo.unidad_medida um ON um.codigo = 'm'
WHERE oc.numero_orden = 'OC-0001'
AND NOT EXISTS (
    SELECT 1 FROM compras.linea_orden_compra lo
    WHERE lo.orden_compra_id = oc.id AND lo.material_id = m.id
);

-- Línea de la OC-0002: 100 hojas de papel
INSERT INTO compras.linea_orden_compra
    (orden_compra_id, material_id, unidad_medida_id, cantidad_solicitada, cantidad_recibida, precio_unitario, moneda, activo, creado_en, actualizado_en)
SELECT oc.id, m.id, um.id, 100.0000, 0, 0.35, 'USD', true, now(), now()
FROM compras.orden_compra oc
JOIN catalogo.material m ON m.codigo = 'MAT-007'
JOIN catalogo.unidad_medida um ON um.codigo = 'pza'
WHERE oc.numero_orden = 'OC-0002'
AND NOT EXISTS (
    SELECT 1 FROM compras.linea_orden_compra lo
    WHERE lo.orden_compra_id = oc.id AND lo.material_id = m.id
);

-- -----------------------------------------------------------------------------
-- 6. Orden de producción piloto con ruta multi-local L01 -> L02 (RF-31):
--    impresión y corte en L01; confección en L02.
-- -----------------------------------------------------------------------------
INSERT INTO produccion.orden_produccion
    (codigo, pedido_venta_id, variante_id, cantidad, local_origen_id, estado, fecha_limite, moneda, activo, creado_en, actualizado_en)
SELECT 'OP-0001', NULL, v.id, 50.0000, l.id, 'EN_PRODUCCION', CURRENT_DATE + 7, 'USD', true, now(), now()
FROM catalogo.variante_producto v
JOIN nucleo.local l ON l.codigo = 'L01'
WHERE v.sku = 'FRANELA-M-BLANCO'
ON CONFLICT (codigo) DO NOTHING;

INSERT INTO produccion.paso_produccion
    (orden_produccion_id, orden_paso, tipo, local_id, trabajador_id, descripcion_tarea, estado, activo, creado_en, actualizado_en)
SELECT op.id, v.orden_paso, v.tipo, l.id, NULL, v.descripcion, v.estado, true, now(), now()
FROM produccion.orden_produccion op
CROSS JOIN (VALUES
    (1, 'IMPRESION',   'L01', 'Impresión de la franela en plóter',        'TERMINADO'),
    (2, 'CORTE',       'L01', 'Corte de la franela en cortadora láser',   'EN_PROCESO'),
    (3, 'CONFECCION',  'L02', 'Confección de la franela en L02',          'PENDIENTE')
) AS v (orden_paso, tipo, cod_local, descripcion, estado)
JOIN nucleo.local l ON l.codigo = v.cod_local
WHERE op.codigo = 'OP-0001'
AND NOT EXISTS (
    SELECT 1 FROM produccion.paso_produccion p
    WHERE p.orden_produccion_id = op.id AND p.orden_paso = v.orden_paso
);

COMMIT;
