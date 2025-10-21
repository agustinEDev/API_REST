# API REST - Usuarios con PostgreSQL | Arquitectura Modular

## 🏗️ Estructura del Proyecto

```
📁 API_REST/
├── app.py                          # 🚀 Aplicación principal Flask
├── .env                            # 🔐 Variables de entorno
├── peticiones.py                   # 🧪 Script para probar la API
├── requirements.txt                # 📦 Dependencias del proyecto
├── GUIA_API_LOCAL_VS_PRODUCCION.md # 📖 Guía completa de arquitectura
├── README.md                       # 📖 Documentación del proyecto
├── 📁 database/
│   ├── __init__.py
│   ├── connection.py               # 🔌 Gestión de conexiones PostgreSQL
│   ├── crear_base_datos_compatible.sql
│   ├── crear_tabla_users_completo.sql
│   └── solucionar_permisos.sql
├── 📁 models/
│   ├── __init__.py
│   └── user_model.py               # 📊 Operaciones CRUD de usuarios
└── 📁 controllers/
    ├── __init__.py
    └── user_controller.py          # 🎛️ Lógica de negocio y endpoints
```

## 🎯 Principios de Arquitectura

### **Separación de Responsabilidades**
- **Database**: Solo manejo de conexiones
- **Models**: Solo operaciones de base de datos (CRUD)
- **Controllers**: Solo lógica de negocio y HTTP
- **App**: Solo configuración de rutas

### **Ventajas de esta Arquitectura**

✅ **Mantenibilidad**: Código organizado y fácil de modificar
✅ **Escalabilidad**: Fácil añadir nuevos modelos y controladores
✅ **Testeo**: Cada capa se puede probar independientemente
✅ **Reutilización**: Los modelos se pueden usar en diferentes contextos
✅ **Limpio**: Separación clara entre capas

## 🚀 Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd API_REST
```

### 2. Crear y activar entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto con tus credenciales de base de datos.

### 5. Ejecutar la aplicación
```bash
python app.py
```

La API estará disponible en `http://localhost:5000`

## 📋 Endpoints Disponibles

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Información del sistema |
| GET | `/usuarios` | Obtener todos los usuarios |
| GET | `/usuarios/<id>` | Obtener usuario por ID |
| POST | `/usuarios` | Crear nuevo usuario |
| PUT | `/usuarios/<id>` | Actualizar usuario completo |
| PATCH | `/usuarios/<id>` | Actualizar usuario parcial |
| DELETE | `/usuarios/<id>` | Eliminar usuario |

## 📊 Flujo de Datos

```
HTTP Request → Controller → Model → Database → PostgreSQL
                    ↓
HTTP Response ← Controller ← Model ← Database ← PostgreSQL
```

## 🔧 Configuración

### Variables de Entorno (.env)
```env
DB_HOST=tu_host_de_base_de_datos
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=tu_usuario_de_db
DB_PASSWORD=tu_contraseña_segura
DB_PORT=5432
```

> ⚠️ **Importante**: Nunca subas el archivo `.env` al repositorio. Agrega `.env` a tu `.gitignore`.

### Dependencias
```bash
pip install flask psycopg2-binary python-dotenv
```

## 🏆 Mejores Prácticas Implementadas

1. **Separación en Capas**: Database → Model → Controller → Routes
2. **Gestión de Errores**: Try/catch en cada capa con mensajes específicos
3. **Validación**: Validación de datos en controllers y models
4. **Configuración Externa**: Variables de entorno para credenciales
5. **Documentación**: Código bien documentado y comentado
6. **Modularidad**: Cada archivo tiene una responsabilidad específica

## 🔄 Extensibilidad

Para añadir nuevas funcionalidades:

1. **Nuevo modelo**: Crear `models/nuevo_model.py`
2. **Nuevo controlador**: Crear `controllers/nuevo_controller.py`  
3. **Nuevas rutas**: Añadir en `app.py`
4. **Nueva conexión**: Extender `database/connection.py`

## 🐛 Troubleshooting

### Error de imports
```bash
# Si hay problemas con imports relativos
export PYTHONPATH="${PYTHONPATH}:/ruta/al/proyecto"
```

### Error de conexión
1. Verificar que PostgreSQL esté corriendo
2. Comprobar variables de entorno en `.env`
3. Ejecutar scripts SQL de configuración

Esta arquitectura modular hace el código más profesional, mantenible y escalable. ¡Perfecto para proyectos en crecimiento! 🎉