-- =============================================================================
-- 00_crear_bd.sql
-- Creación de la base de datos de desarrollo de DLL Sublimados.
--
-- Uso (desde la raíz del repositorio con tu superusuario de PostgreSQL):
--   psql -U postgres -f database/00_crear_bd.sql
--
-- Requisito: un servidor PostgreSQL 14+ accesible en localhost:5432.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Base de datos del proyecto.
--    El nombre va en minúsculas y snake_case: evita tener que entrecomillarlo.
-- -----------------------------------------------------------------------------
-- Si la base ya existe, recrearla desde la terminal con:
--   dropdb -U postgres dll_sublimados && createdb -U postgres -O postgres dll_sublimados
CREATE DATABASE dll_sublimados
    OWNER postgres
    ENCODING 'UTF8'
    LC_COLLATE 'C.UTF-8'
    LC_CTYPE 'C.UTF-8';

-- -----------------------------------------------------------------------------
-- 2. Comprobación de conexión.
-- -----------------------------------------------------------------------------
\connect dll_sublimados
SELECT current_database(), current_user, version();
