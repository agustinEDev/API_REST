-- Script para solucionar permisos en PostgreSQL
-- Ejecutar como superusuario (postgres) conectado a la base usuarios_app

-- ===============================================
-- SOLUCIÓN DE PERMISOS
-- ===============================================

-- Verificar conexión actual
SELECT 
    current_database() as base_datos,
    current_user as usuario_actual,
    'Debe mostrar usuarios_app y postgres' as verificacion;

-- Otorgar todos los permisos necesarios al usuario app_user
GRANT ALL PRIVILEGES ON SCHEMA public TO app_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO app_user;

-- Otorgar permisos sobre objetos futuros
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT ALL PRIVILEGES ON TABLES TO app_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT ALL PRIVILEGES ON SEQUENCES TO app_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT ALL PRIVILEGES ON FUNCTIONS TO app_user;

-- Hacer a app_user propietario del esquema public (opcional)
ALTER SCHEMA public OWNER TO app_user;

-- Verificar que los permisos se otorgaron correctamente
SELECT 
    '✅ Permisos otorgados correctamente' as mensaje,
    'Schema public configurado' as estado;

-- Verificar información del esquema
SELECT 
    '📋 Información del esquema public:' as info,
    nspname as nombre_esquema,
    pg_catalog.pg_get_userbyid(nspowner) as propietario
FROM pg_namespace 
WHERE nspname = 'public';

-- Mostrar permisos actuales del usuario
SELECT 
    '🔐 Permisos de app_user:' as info,
    has_schema_privilege('app_user', 'public', 'CREATE') as puede_crear,
    has_schema_privilege('app_user', 'public', 'USAGE') as puede_usar;

-- Información para el siguiente paso
SELECT 
    '🚀 Ahora puedes:' as paso_1,
    '1. Conectarte como app_user a usuarios_app' as paso_2,
    '2. Ejecutar crear_tabla_users_completo.sql' as paso_3;