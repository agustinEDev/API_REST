# API REST - Usuarios con PostgreSQL | Arquitectura Modular

Una API REST completa con arquitectura modular, cliente interactivo y mejores prácticas de desarrollo.

## 🏗️ Estructura del Proyecto

```
📁 API_REST/
├── api.py                          # 🚀 Servidor API REST (Flask)
├── main.py                         # 🎮 Cliente interactivo con menú
├── .env                            # 🔐 Variables de entorno
├── requirements.txt                # 📦 Dependencias del proyecto
├── COMANDOS.md                     # 🛠️ Guía de comandos útiles
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

## 🎯 Componentes Principales

### **🚀 Servidor API (`api.py`)**
- **Framework**: Flask con arquitectura modular
- **Puerto**: 8000 (configurable)
- **Funcionalidad**: Expone endpoints REST para gestión de usuarios
- **Separación**: Database → Models → Controllers → Routes

### **🎮 Cliente Interactivo (`main.py`)**
- **Interfaz**: Menú interactivo de línea de comandos
- **Funcionalidad**: Cliente completo para probar todos los endpoints
- **Características**:
  - ✅ Validación de conexión automática
  - ✅ Manejo robusto de errores
  - ✅ Interfaz visual con emojis
  - ✅ Validación de entrada de datos
  - ✅ Confirmación para operaciones críticas

### **Ventajas de esta Arquitectura**

- ✅ **Separación clara**: Servidor y cliente independientes
- ✅ **Mantenibilidad**: Código organizado y documentado
- ✅ **Escalabilidad**: Fácil añadir nuevos endpoints y funciones
- ✅ **Testeo**: Cliente robusto para pruebas completas
- ✅ **Experiencia de usuario**: Interfaz intuitiva y segura

## 🚀 Inicio Rápido

### 1. Clonar e instalar
```bash
git clone <url-del-repositorio>
cd API_REST
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar base de datos
Crea un archivo `.env` con tus credenciales:
```env
DB_HOST=tu_host_de_base_de_datos
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=tu_usuario_de_db
DB_PASSWORD=tu_contraseña_segura
DB_PORT=5432
```

### 3. Ejecutar el servidor API
```bash
python api.py
```
El servidor estará disponible en `http://localhost:8000`

### 4. Usar el cliente interactivo
En otra terminal:
```bash
python main.py
```

¡Y ya puedes interactuar con tu API a través del menú! 🎉

## 🎮 Cliente Interactivo - Funcionalidades

El cliente `main.py` ofrece un menú completo para interactuar con la API:

```
==================================================
🌐 CLIENTE API REST - GESTIÓN DE USUARIOS
==================================================
1. Obtener todos los usuarios
2. Obtener usuario por ID
3. Crear nuevo usuario
4. Actualizar usuario completo
5. Actualizar usuario parcialmente
6. Eliminar usuario
7. Salir
==================================================
```

### **Características del Cliente:**
- ✅ **Verificación automática** de conexión con la API
- ✅ **Validación de entrada** para todos los campos
- ✅ **Manejo de errores** con mensajes informativos
- ✅ **Confirmaciones** para operaciones críticas (eliminación)
- ✅ **Campos opcionales** en creación y actualización
- ✅ **Formateo JSON** legible para las respuestas
- ✅ **Interfaz visual** con emojis y colores conceptuales

## 📋 Endpoints API

| Método | Ruta | Función del Cliente | Descripción |
|--------|------|-------------------|-------------|
| GET | `/` | Verificación inicial | Información del sistema |
| GET | `/usuarios` | Opción 1 | Obtener todos los usuarios |
| GET | `/usuarios/<id>` | Opción 2 | Obtener usuario por ID |
| POST | `/usuarios` | Opción 3 | Crear nuevo usuario |
| PUT | `/usuarios/<id>` | Opción 4 | Actualizar usuario completo |
| PATCH | `/usuarios/<id>` | Opción 5 | Actualizar usuario parcial |
| DELETE | `/usuarios/<id>` | Opción 6 | Eliminar usuario (con confirmación) |

## 📊 Flujo Completo

```
Cliente (main.py) → HTTP Request → API (api.py) → Controller → Model → Database
                                       ↓
Cliente (main.py) ← HTTP Response ← API (api.py) ← Controller ← Model ← Database
```

## ⚡ Ejemplo de Uso

### **1. Iniciar el servidor**
```bash
$ python api.py
� Iniciando servidor Flask con PostgreSQL (Arquitectura Modular)...
📊 Configuración de PostgreSQL:
   Host: localhost
   Database: usuarios_app
   User: app_user
   Port: 5432
🚀 Servidor iniciado en http://localhost:8000
```

### **2. Ejecutar el cliente**
```bash
$ python main.py
🚀 Iniciando cliente API REST...
✅ Conexión con la API establecida correctamente.

==================================================
🌐 CLIENTE API REST - GESTIÓN DE USUARIOS
==================================================
1. Obtener todos los usuarios
2. Obtener usuario por ID
3. Crear nuevo usuario
4. Actualizar usuario completo
5. Actualizar usuario parcialmente
6. Eliminar usuario
7. Salir
==================================================

🎯 Seleccione una opción: 3
```

### **3. Crear un usuario**
```bash
🔄 Ejecutando: Crear nuevo usuario

📝 Creando nuevo usuario:
📝 Ingrese el nombre del usuario: Juan
📝 Ingrese el apellido del usuario: Pérez
📝 Ingrese el email del usuario: juan@email.com
📝 Ingrese la edad del usuario: 25

📋 Respuesta de la API:
------------------------------
{
  "mensaje": "Usuario creado exitosamente",
  "usuario": {
    "id": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan@email.com",
    "edad": 25
  }
}
------------------------------
```

## 🏆 Características Avanzadas

### **🛡️ Manejo de Errores Robusto**
```bash
❌ Error: No se pudo conectar con la API en http://localhost:8000
💡 Asegúrese de que el servidor Flask esté ejecutándose.
```

### **✅ Validación de Datos**
- Campos obligatorios vs opcionales
- Validación de tipos (enteros, strings)
- Confirmación para operaciones críticas

### **🎨 Interfaz de Usuario**
- Menús visuales con emojis
- Respuestas JSON formateadas
- Mensajes informativos y de error
- Progreso de operaciones

### **⚙️ Configuración Flexible**
- URL base configurable
- Timeout personalizable
- Variables de entorno seguras

## 🔄 Extensibilidad

### **Para el Servidor (`api.py`):**
1. **Nuevo modelo**: Crear `models/nuevo_model.py`
2. **Nuevo controlador**: Crear `controllers/nuevo_controller.py`  
3. **Nuevas rutas**: Añadir endpoints en `api.py`

### **Para el Cliente (`main.py`):**
1. **Nueva función**: Añadir método en `APIClient`
2. **Nueva opción**: Agregar al diccionario `opciones`
3. **Nueva validación**: Extender métodos de entrada

## 📚 Documentación Adicional

- **📁 `COMANDOS.md`**: Guía completa de comandos útiles
- **📁 `GUIA_API_LOCAL_VS_PRODUCCION.md`**: Arquitectura y deployment
- **🔍 Comentarios en código**: Documentación inline completa

## 🐛 Solución de Problemas

### **El cliente no conecta:**
```bash
# 1. Verificar que el servidor esté corriendo
python api.py

# 2. Verificar el puerto en otra terminal
lsof -i :8000

# 3. Probar conexión manual
curl http://localhost:8000/
```

### **Error de base de datos:**
1. ✅ PostgreSQL esté ejecutándose
2. ✅ Variables de entorno en `.env` sean correctas  
3. ✅ Tablas creadas con los scripts SQL

¡Una API REST completa con cliente interactivo y mejores prácticas profesionales! 🚀