-- Script completo: Crear tabla users con datos
-- Ejecutar después de crear_base_datos.sql
-- IMPORTANTE: Conectar primero a la base de datos usuarios_app en DBeaver

-- ===============================================
-- PARTE 2: CREAR TABLA Y POBLAR CON DATOS
-- ===============================================

-- Verificar que estamos en la base de datos correcta
SELECT 
    current_database() as base_datos_actual,
    'Debes estar conectado a usuarios_app' as verificacion;

-- Eliminar la tabla si existe (para poder recrearla)
DROP TABLE IF EXISTS users CASCADE;

-- Crear la tabla users con todos los campos necesarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    email VARCHAR(150) NOT NULL UNIQUE,
    edad INTEGER CHECK (edad >= 0 AND edad <= 150),
    telefono VARCHAR(20),
    ciudad VARCHAR(100),
    pais VARCHAR(100) DEFAULT 'España',
    activo BOOLEAN DEFAULT true,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Campos adicionales útiles
    genero VARCHAR(20) CHECK (genero IN ('Masculino', 'Femenino', 'Otro', 'Prefiero no decir')),
    profesion VARCHAR(150),
    salario DECIMAL(10,2),
    -- Campos de metadatos
    created_by VARCHAR(100) DEFAULT 'system',
    notas TEXT
);

-- Crear índices para mejorar rendimiento en consultas frecuentes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_ciudad ON users(ciudad);
CREATE INDEX idx_users_activo ON users(activo);
CREATE INDEX idx_users_fecha_registro ON users(fecha_registro);
CREATE INDEX idx_users_nombre_apellido ON users(nombre, apellido);

-- Crear función para actualizar fecha_actualizacion automáticamente
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger para actualizar fecha_actualizacion automáticamente
CREATE TRIGGER trigger_actualizar_fecha
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

-- ===============================================
-- INSERTAR DATOS DE EJEMPLO VARIADOS
-- ===============================================

-- Usuarios activos con datos completos
INSERT INTO users (nombre, apellido, email, edad, telefono, ciudad, genero, profesion, salario) VALUES
    ('Juan', 'Pérez González', 'juan.perez@email.com', 28, '+34-666-111-111', 'Madrid', 'Masculino', 'Desarrollador Web', 45000.00),
    ('María', 'García López', 'maria.garcia@email.com', 32, '+34-666-222-222', 'Barcelona', 'Femenino', 'Diseñadora UX/UI', 42000.00),
    ('Pedro', 'López Martín', 'pedro.lopez@email.com', 25, '+34-666-333-333', 'Valencia', 'Masculino', 'Analista de Datos', 38000.00),
    ('Ana', 'Martín Ruiz', 'ana.martin@email.com', 29, '+34-666-444-444', 'Sevilla', 'Femenino', 'Project Manager', 48000.00),
    ('Carlos', 'Ruiz Sánchez', 'carlos.ruiz@email.com', 35, '+34-666-555-555', 'Bilbao', 'Masculino', 'DevOps Engineer', 52000.00),
    ('Laura', 'Sánchez Torres', 'laura.sanchez@email.com', 27, '+34-666-666-666', 'Madrid', 'Femenino', 'Marketing Digital', 35000.00),
    ('Miguel', 'Torres Flores', 'miguel.torres@email.com', 31, '+34-666-777-777', 'Barcelona', 'Masculino', 'Arquitecto Software', 55000.00),
    ('Carmen', 'Flores Castro', 'carmen.flores@email.com', 26, '+34-666-888-888', 'Valencia', 'Femenino', 'Consultora IT', 40000.00),
    ('Roberto', 'Castro Moreno', 'roberto.castro@email.com', 33, '+34-666-999-999', 'Sevilla', 'Masculino', 'Scrum Master', 46000.00),
    ('Isabel', 'Moreno Herrera', 'isabel.moreno@email.com', 30, '+34-666-000-000', 'Zaragoza', 'Femenino', 'Data Scientist', 50000.00),
    ('Diego', 'Herrera Jiménez', 'diego.herrera@email.com', 24, '+34-666-111-222', 'Madrid', 'Masculino', 'Frontend Developer', 36000.00),
    ('Sofía', 'Jiménez Vargas', 'sofia.jimenez@email.com', 28, '+34-666-333-444', 'Barcelona', 'Femenino', 'Backend Developer', 44000.00),
    ('Andrés', 'Vargas Romero', 'andres.vargas@email.com', 36, '+34-666-555-666', 'Valencia', 'Masculino', 'Tech Lead', 58000.00),
    ('Patricia', 'Romero Gil', 'patricia.romero@email.com', 29, '+34-666-777-888', 'Málaga', 'Femenino', 'Product Owner', 47000.00),
    ('Fernando', 'Gil Mendoza', 'fernando.gil@email.com', 34, '+34-666-999-000', 'Murcia', 'Masculino', 'CTO', 75000.00);

-- Usuarios con algunos campos opcionales vacíos
INSERT INTO users (nombre, apellido, email, edad, ciudad, genero, activo) VALUES
    ('Lucía', 'Mendoza Silva', 'lucia.mendoza@email.com', 23, 'Santander', 'Femenino', true),
    ('Javier', 'Silva Ortega', 'javier.silva@email.com', 31, 'Granada', 'Masculino', true),
    ('Elena', 'Ortega Ramos', 'elena.ortega@email.com', 27, 'Córdoba', 'Femenino', true);

-- Usuarios inactivos para testing
INSERT INTO users (nombre, apellido, email, edad, ciudad, activo, notas) VALUES
    ('Usuario', 'Inactivo Uno', 'inactivo1@email.com', 40, 'Madrid', false, 'Usuario desactivado por inactividad'),
    ('Usuario', 'Inactivo Dos', 'inactivo2@email.com', 45, 'Barcelona', false, 'Cuenta suspendida temporalmente');

-- Usuarios con géneros diversos
INSERT INTO users (nombre, apellido, email, edad, ciudad, genero, profesion) VALUES
    ('Alex', 'Rodríguez Vega', 'alex.rodriguez@email.com', 26, 'Alicante', 'Otro', 'Diseñador Gráfico'),
    ('Jordan', 'Vega Morales', 'jordan.vega@email.com', 30, 'Vigo', 'Prefiero no decir', 'Consultor');

-- ===============================================
-- VERIFICACIONES Y ESTADÍSTICAS
-- ===============================================

-- Verificar que los datos se insertaron correctamente
SELECT '📊 ESTADÍSTICAS DE LA TABLA USERS' as titulo;

SELECT 
    '📈 Resumen General' as categoria,
    COUNT(*) as total_usuarios,
    COUNT(CASE WHEN activo = true THEN 1 END) as usuarios_activos,
    COUNT(CASE WHEN activo = false THEN 1 END) as usuarios_inactivos,
    ROUND(AVG(edad), 1) as edad_promedio
FROM users;

-- Mostrar distribución por género
SELECT '👥 Distribución por Género:' as titulo;
SELECT 
    COALESCE(genero, 'Sin especificar') as genero,
    COUNT(*) as cantidad,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 1) as porcentaje
FROM users 
GROUP BY genero 
ORDER BY cantidad DESC;

-- Mostrar distribución por ciudad
SELECT '🏙️ Distribución por Ciudad:' as titulo;
SELECT 
    ciudad, 
    COUNT(*) as total_usuarios,
    COUNT(CASE WHEN activo = true THEN 1 END) as activos,
    ROUND(AVG(edad), 1) as edad_promedio
FROM users 
GROUP BY ciudad 
ORDER BY total_usuarios DESC;

-- Mostrar usuarios con salarios más altos
SELECT '💰 Top 5 Salarios:' as titulo;
SELECT 
    nombre || ' ' || apellido as nombre_completo,
    profesion,
    salario,
    ciudad
FROM users 
WHERE salario IS NOT NULL 
ORDER BY salario DESC 
LIMIT 5;

-- Mostrar algunos usuarios de ejemplo
SELECT '👤 Muestra de usuarios (primeros 10):' as titulo;
SELECT 
    id, 
    nombre || ' ' || COALESCE(apellido, '') as nombre_completo,
    email, 
    edad, 
    ciudad, 
    CASE WHEN activo THEN '✅ Activo' ELSE '❌ Inactivo' END as estado,
    TO_CHAR(fecha_registro, 'DD/MM/YYYY HH24:MI') as fecha_registro
FROM users 
ORDER BY id 
LIMIT 10;

-- Otorgar permisos específicos al usuario de la aplicación
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE users TO app_user;
GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO app_user;

-- Resumen final
SELECT 
    '✅ Tabla users creada y poblada exitosamente' as status,
    '🔐 Permisos otorgados al usuario app_user' as permisos,
    COUNT(*) as total_registros_insertados
FROM users;

SELECT 
    '🚀 ¡Listo para usar con tu aplicación Flask!' as mensaje,
    'DB_NAME=usuarios_app' as config_1,
    'DB_USER=app_user' as config_2,
    'DB_PASSWORD=PruebaDatabase123.' as config_3;