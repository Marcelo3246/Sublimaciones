-- =============================================================================
-- 02_tasa_cambio.sql
-- Registra el tipo de cambio inicial USD → Bs.
--
-- Requiere que ya exista un usuario administrador (created con
-- `python manage.py createsuperuser`), porque la serie de tipos de cambio
-- guarda quién la registró (RNF-05).
--
-- Uso:
--   psql -U postgres -d dll_sublimados -f database/02_tasa_cambio.sql
-- =============================================================================

INSERT INTO nucleo.tasa_cambio (
    fecha_vigencia, dolares_a_bs, registrado_por_id, creado_en, actualizado_en, activo
)
SELECT CURRENT_DATE, 36.50, u.id, now(), now(), true
FROM nucleo.usuario u
WHERE u.is_superuser
ORDER BY u.id
LIMIT 1
ON CONFLICT DO NOTHING;

-- Comprobación:
--   SELECT fecha_vigencia, dolares_a_bs FROM nucleo.tasa_cambio ORDER BY fecha_vigencia DESC LIMIT 5;
