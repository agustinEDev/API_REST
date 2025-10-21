-- Script completo para PostgreSQL: Crear base de datos y tabla users
-- VERSIÓN COMPATIBLE - Ejecutar como superusuario (postgres) desde DBeaver

-- ===============================================
-- PARTE 1: CREAR BASE DE DATOS Y USUARIO
-- ===============================================

-- Crear la base de datos si no existe (versión compatible)
DROP DATABASE IF EXISTS usuarios_app;

-- Opción 1: Con collation en español (si está disponible)
-- Si da error, usa la Opción 2
CREATE DATABASE usuarios_app
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    TEMPLATE = template0
    LC_COLLATE = 'es_ES.UTF-8'
    LC_CTYPE = 'es_ES.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

/*
-- Opción 2: Versión compatible universal (descomenta si la Opción 1 falla)
CREATE DATABASE usuarios_app
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    TEMPLATE = template0
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
*/

-- Crear usuario específico para la aplicación (opcional pero recomendado)
DROP USER IF EXISTS app_user;
CREATE USER app_user WITH
    LOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    INHERIT
    NOREPLICATION
    CONNECTION LIMIT -1
    PASSWORD 'PruebaDatabase123.';

-- Otorgar permisos al usuario sobre la base de datos
GRANT CONNECT ON DATABASE usuarios_app TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT CREATE ON SCHEMA public TO app_user;

-- Comentario informativo
COMMENT ON DATABASE usuarios_app IS 'Base de datos para aplicación de gestión de usuarios';

-- Verificar la creación (compatible con DBeaver)
SELECT 
    '✅ Base de datos usuarios_app creada exitosamente' as mensaje,
    current_database() as base_datos_actual,
    current_user as usuario_actual;

-- Mostrar información del nuevo usuario
SELECT 
    usename as usuario_creado,
    usesuper as es_superusuario,
    usecreatedb as puede_crear_db,
    '👤 Usuario app_user creado con contraseña PruebaDatabase123.' as info
FROM pg_user 
WHERE usename = 'app_user';

-- Información para conectarse
SELECT 
    '🔗 Para conectarse desde DBeaver:' as paso_1,
    '   Host: localhost' as paso_2,
    '   Database: usuarios_app' as paso_3,
    '   User: app_user' as paso_4,
    '   Password: PruebaDatabase123.' as paso_5,
    '📋 Después ejecuta crear_tabla_users_completo.sql' as paso_6;

-- Verificar collations disponibles en tu sistema
SELECT 
    '📋 Collations disponibles en tu sistema:' as info;
SELECT 
    collname as collation_disponible,
    collcollate as lc_collate,
    collctype as lc_ctype
FROM pg_collation 
WHERE collname LIKE '%es%' OR collname LIKE '%utf%' OR collname = 'C'
ORDER BY collname
LIMIT 10;