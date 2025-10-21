# api.py
from flask import Flask, jsonify
import sys
import os

# Añadir el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.connection import DatabaseConnection
from controllers.user_controller import UserController

app = Flask(__name__)

# Inicializar controlador
user_controller = UserController()

# ===== VALIDADORES =====

def validar_id_usuario(usuario_id):
    """Valida que el ID de usuario sea válido."""
    if usuario_id is None:
        return False, "ID requerido"
    
    try:
        id_int = int(usuario_id)
        if id_int <= 0:
            return False, "ID debe ser mayor a 0"
        return True, id_int
    except (ValueError, TypeError):
        return False, "ID inválido"

# ===== RUTAS (ENDPOINTS) =====

# Endpoint de información del sistema
@app.route('/', methods=['GET'])
def inicio():
    return user_controller.obtener_info_sistema()

# Endpoints de usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return user_controller.obtener_todos()

@app.route('/usuarios/<usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    valido, resultado = validar_id_usuario(usuario_id)
    if not valido:
        return jsonify({"exito": False, "error": resultado}), 400
    return user_controller.obtener_por_id(resultado)

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    return user_controller.crear()

@app.route('/usuarios/<usuario_id>', methods=['PUT'])
def actualizar_usuario(usuario_id):
    valido, resultado = validar_id_usuario(usuario_id)
    if not valido:
        return jsonify({"exito": False, "error": resultado}), 400
    return user_controller.actualizar(resultado)

@app.route('/usuarios/<usuario_id>', methods=['PATCH'])
def actualizar_parcial_usuario(usuario_id):
    valido, resultado = validar_id_usuario(usuario_id)
    if not valido:
        return jsonify({"exito": False, "error": resultado}), 400
    return user_controller.actualizar_parcial(resultado)

@app.route('/usuarios/<usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    valido, resultado = validar_id_usuario(usuario_id)
    if not valido:
        return jsonify({"exito": False, "error": resultado}), 400
    return user_controller.eliminar(resultado)

@app.route('/usuarios/paginado', methods=['GET'])
def obtener_usuarios_paginados():
    return user_controller.obtener_paginados()

# ===== CONFIGURACIÓN E INICIO =====

if __name__ == '__main__':
    print("🐘 Iniciando servidor Flask con PostgreSQL (Arquitectura Modular)...")
    
    # Crear instancia de conexión para validar
    db = DatabaseConnection()
    
    # Verificar configuración de variables de entorno
    if not db.validar_configuracion():
        print("❌ No se puede iniciar el servidor sin la configuración completa.")
        exit(1)
    
    # Mostrar configuración
    config_info = db.get_config_info()
    print(f"📊 Configuración de PostgreSQL:")
    print(f"   Host: {config_info['host']}")
    print(f"   Database: {config_info['database']}")
    print(f"   User: {config_info['user']}")
    print(f"   Port: {config_info['port']}")
    
    # Verificar que la base de datos esté lista
    if db.verificar_tabla_existe():
        print("🚀 Servidor iniciado en http://localhost:8000")
        print("📋 Endpoints disponibles:")
        print("   GET    http://localhost:8000/")
        print("   GET    http://localhost:8000/usuarios")
        print("   GET    http://localhost:8000/usuarios/1")
        print("   POST   http://localhost:8000/usuarios")
        print("   PUT    http://localhost:8000/usuarios/1")
        print("   PATCH  http://localhost:8000/usuarios/1")
        print("   DELETE http://localhost:8000/usuarios/1")
        print("\n🏗️ Arquitectura Modular:")
        print("   📁 database/connection.py - Gestión de conexiones")
        print("   📁 models/user_model.py - Operaciones de base de datos")
        print("   📁 controllers/user_controller.py - Lógica de negocio")
        print("   📁 api.py - Rutas y configuración")
        
        # Agregar error handler para método no permitido
        @app.errorhandler(405)
        def metodo_no_permitido(error):
            """Maneja errores de método no permitido."""
            return jsonify({
                "exito": False,
                "error": "Método no permitido"
            }), 405
        
        app.run(debug=True, port=8000)
    else:
        print("❌ No se pudo inicializar la base de datos.")
        print("📋 Verifica que:")
        print("   1. PostgreSQL esté corriendo")
        print("   2. La base de datos 'usuarios_app' exista")
        print("   3. El usuario 'app_user' tenga permisos")
        print("   4. Hayas ejecutado los scripts SQL")