# controllers/user_controller.py
from flask import jsonify, request
from models.user_model import UserModel

class UserController:
    """Controlador para manejar las operaciones de usuarios"""
    
    def __init__(self):
        self.user_model = UserModel()
    
    def obtener_todos(self):
        """GET /usuarios - Obtener todos los usuarios"""
        try:
            usuarios = self.user_model.obtener_todos()
            return jsonify(usuarios)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def obtener_por_id(self, usuario_id):
        """GET /usuarios/<id> - Obtener un usuario por ID"""
        try:
            usuario = self.user_model.obtener_por_id(usuario_id)
            if usuario:
                return jsonify(usuario)
            else:
                return jsonify({"error": "Usuario no encontrado"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def crear(self):
        """POST /usuarios - Crear nuevo usuario"""
        datos = request.get_json()
        
        # Validar datos requeridos
        if not datos or not datos.get('nombre') or not datos.get('email'):
            return jsonify({"error": "Nombre y email son requeridos"}), 400
        
        try:
            nuevo_usuario = self.user_model.crear(datos)
            return jsonify(nuevo_usuario), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def actualizar(self, usuario_id):
        """PUT /usuarios/<id> - Actualizar usuario completo"""
        datos = request.get_json()
        
        if not datos:
            return jsonify({"error": "No hay datos para actualizar"}), 400
        
        try:
            usuario_actualizado = self.user_model.actualizar(usuario_id, datos)
            return jsonify(usuario_actualizado)
        except ValueError as e:
            if "no encontrado" in str(e).lower():
                return jsonify({"error": str(e)}), 404
            else:
                return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def actualizar_parcial(self, usuario_id):
        """PATCH /usuarios/<id> - Actualizar usuario parcial"""
        datos = request.get_json()
        
        if not datos:
            return jsonify({"error": "No hay datos para actualizar"}), 400
        
        try:
            resultado = self.user_model.actualizar_parcial(usuario_id, datos)
            return jsonify(resultado)
        except ValueError as e:
            if "no encontrado" in str(e).lower():
                return jsonify({"error": str(e)}), 404
            else:
                return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def eliminar(self, usuario_id):
        """DELETE /usuarios/<id> - Eliminar usuario"""
        try:
            resultado = self.user_model.eliminar(usuario_id)
            return jsonify(resultado)
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def obtener_info_sistema(self):
        """GET / - Obtener información del sistema y estadísticas"""
        try:
            estadisticas = self.user_model.obtener_estadisticas()
            db_config = self.user_model.db.get_config_info()
            
            return jsonify({
                "mensaje": "API de Usuarios con PostgreSQL",
                "base_datos": "PostgreSQL",
                "version_postgresql": estadisticas["version_postgresql"],
                "total_usuarios": estadisticas["total_usuarios"],
                "configuracion": {
                    "host": db_config['host'],
                    "database": db_config['database'],
                    "puerto": db_config['port']
                },
                "endpoints": {
                    "GET /usuarios": "Obtener todos los usuarios",
                    "GET /usuarios/<id>": "Obtener usuario por ID",
                    "POST /usuarios": "Crear nuevo usuario",
                    "PUT /usuarios/<id>": "Actualizar usuario completo",
                    "PATCH /usuarios/<id>": "Actualizar usuario parcial",
                    "DELETE /usuarios/<id>": "Eliminar usuario"
                }
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500