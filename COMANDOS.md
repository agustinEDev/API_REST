# 🛠️ Comandos Útiles - API REST

## 🚀 Gestión del Servidor Flask

### **Arrancar el servidor**
```bash
# Método normal (primer plano)
python api.py

# Método background (sigue corriendo aunque cierres terminal)
python api.py &

# Con modo debug (reinicia automáticamente en cambios)
export FLASK_ENV=development
python api.py
```

### **Parar el servidor**
```bash
# Método 1: Si está en primer plano
Ctrl + C

# Método 2: Si está en background
lsof -i :8000                    # Ver qué usa el puerto 8000
kill -9 [PID]                    # Matar proceso específico

# Método 3: Matar proceso específico de la app
pkill -f "python api.py"         # Mata específicamente api.py
```

### **Verificar estado del servidor**
```bash
# Ver si está corriendo
lsof -i :8000

# Ver todos los procesos Python
ps aux | grep python

# Probar si responde
curl http://localhost:8000/
```

### **Comandos rápidos**
```bash
# Parar y arrancar en una línea
pkill -f "python api.py" && python api.py

# Verificar que arrancó correctamente
python api.py & sleep 2 && curl http://localhost:8000/
```

---

## 🐍 Gestión del Entorno Python

### **Entorno virtual**
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate          # Windows

# Desactivar entorno virtual
deactivate
```

### **Dependencias**
```bash
# Instalar dependencias del proyecto
pip install -r requirements.txt

# Instalar paquete específico
pip install nombre_paquete

# Actualizar requirements.txt
pip freeze > requirements.txt

# Ver paquetes instalados
pip list
```

---

## 📊 Gestión de Base de Datos

### **PostgreSQL**
```bash
# Conectar a PostgreSQL
psql -h localhost -U app_user -d usuarios_app

# Ejecutar script SQL
psql -h localhost -U app_user -d usuarios_app -f database/crear_tabla_users_completo.sql

# Ver tablas
\dt

# Salir de psql
\q
```

### **Comandos SQL útiles**
```sql
-- Ver todos los usuarios
SELECT * FROM users;

-- Contar usuarios
SELECT COUNT(*) FROM users;

-- Eliminar todos los datos (¡CUIDADO!)
TRUNCATE TABLE users;
```

---

## 🧪 Pruebas y Testing

### **Ejecutar cliente de pruebas**
```bash
# Ejecutar cliente de pruebas
python main.py

# Ejecutar con salida detallada
python -v main.py
```

### **Nuevas Funcionalidades del Cliente**
```bash
# Opción 1: Ver todos los usuarios (formato JSON)
# Opción 2: Navegación paginada (usuario por usuario)
# Opción 3: Obtener usuario específico por ID
# Opción 4: Crear nuevo usuario
# Opción 5: Actualizar usuario completo
# Opción 6: Actualizar usuario parcial
# Opción 7: Eliminar usuario
# Opción 8: Salir
```

### **Controles de Navegación Paginada**
```bash
# Dentro de la opción 2 (usuarios paginados):
Enter         # Siguiente usuario
q + Enter     # Volver al menú principal  
help + Enter  # Mostrar ayuda
Ctrl+C        # Cancelar operación inmediatamente
```

### **Curl para probar endpoints**
```bash
# Obtener todos los usuarios
curl http://localhost:8000/usuarios

# Obtener usuario específico
curl http://localhost:8000/usuarios/1

# Crear nuevo usuario
curl -X POST http://localhost:8000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Juan", "email": "juan@email.com", "edad": 25}'

# Actualizar usuario
curl -X PUT http://localhost:8000/usuarios/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Juan Actualizado", "email": "juan@email.com", "edad": 26}'

# Eliminar usuario
curl -X DELETE http://localhost:8000/usuarios/1
```

---

## 📂 Git y Control de Versiones

### **Comandos básicos**
```bash
# Ver estado del repositorio
git status

# Ver ramas disponibles
git branch -vv

# Cambiar de rama
git checkout nombre-rama

# Crear nueva rama
git checkout -b nueva-rama

# Ver remotes configurados
git remote -v
```

### **Sincronización**
```bash
# Obtener cambios del remoto
git pull

# Subir cambios
git add .
git commit -m "Descripción del cambio"
git push

# Subir nueva rama
git push --set-upstream origin nombre-rama
```

### **Limpiar archivos ignorados**
```bash
# Eliminar archivos del seguimiento (pero mantener en disco)
git rm -r --cached nombre_archivo

# Eliminar carpetas __pycache__ del seguimiento
git rm -r --cached controllers/__pycache__ database/__pycache__ models/__pycache__
```

---

## 🔧 Utilidades del Sistema

### **Gestión de procesos**
```bash
# Ver procesos que usan un puerto específico
lsof -i :8000

# Matar proceso por PID
kill -9 [PID]

# Ver procesos Python activos
ps aux | grep python
```

### **Archivos y directorios**
```bash
# Ver estructura del proyecto
tree                             # Si tienes tree instalado
ls -la                          # Ver archivos ocultos

# Buscar archivos
find . -name "*.py"             # Buscar archivos Python
grep -r "texto" .               # Buscar texto en archivos
```

---

## 🚨 Solución de Problemas Comunes

### **Puerto en uso**
```bash
# Error: "Address already in use"
lsof -i :8000                   # Ver qué usa el puerto
kill -9 [PID]                  # Matar el proceso
python api.py                  # Reintentar
```

### **Problemas de imports**
```bash
# Si hay problemas con imports relativos
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python api.py
```

### **Base de datos no conecta**
```bash
# Verificar que PostgreSQL esté corriendo
brew services list | grep postgresql    # En macOS con Homebrew
sudo service postgresql status          # En Linux

# Verificar variables de entorno
cat .env
```

### **Limpiar cache de Python**
```bash
# Eliminar archivos __pycache__
find . -type d -name "__pycache__" -exec rm -r {} +

# Eliminar archivos .pyc
find . -name "*.pyc" -delete
```

---

## 📋 Checklist de Desarrollo

### **Antes de empezar a trabajar:**
- [ ] `source .venv/bin/activate` - Activar entorno virtual
- [ ] `git pull` - Obtener últimos cambios
- [ ] `python api.py` - Arrancar servidor
- [ ] `python main.py` - Verificar que todo funciona
- [ ] Probar opción 2 (navegación paginada) - Nueva funcionalidad

### **Antes de hacer commit:**
- [ ] `Ctrl + C` - Parar servidor
- [ ] `git status` - Ver cambios
- [ ] `git add .` - Añadir cambios
- [ ] `git commit -m "mensaje descriptivo"` - Hacer commit
- [ ] `git push` - Subir cambios

### **Limpieza periódica:**
- [ ] `find . -type d -name "__pycache__" -exec rm -r {} +` - Limpiar cache
- [ ] `pip freeze > requirements.txt` - Actualizar dependencias
- [ ] `git rm -r --cached archivos_innecesarios` - Limpiar Git

---

**Fecha de creación:** 21 de octubre de 2025  
**Última actualización:** 21 de octubre de 2025 - Agregada navegación paginada  
**Proyecto:** API de Usuarios con PostgreSQL - Comandos de Referencia