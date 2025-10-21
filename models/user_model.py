# models/user_model.py
import psycopg2
import psycopg2.extras
from database.connection import DatabaseConnection

class UserModel:
    """Modelo para operaciones CRUD de usuarios"""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def obtener_todos(self):
        """Obtener todos los usuarios"""
        conn = self.db.obtener_conexion()
        if not conn:
            raise Exception("Error de conexión a la base de datos")
        
        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute('''
                SELECT id, nombre, apellido, email, edad, telefono, ciudad, 
                       activo, fecha_registro, fecha_actualizacion, genero, 
                       profesion, salario
                FROM users 
                ORDER BY id
            ''')
            usuarios = [dict(row) for row in cursor.fetchall()]
            
            # Convertir timestamps a string para JSON
            for usuario in usuarios:
                if usuario['fecha_registro']:
                    usuario['fecha_registro'] = usuario['fecha_registro'].isoformat()
                if usuario['fecha_actualizacion']:
                    usuario['fecha_actualizacion'] = usuario['fecha_actualizacion'].isoformat()
            
            conn.close()
            return usuarios
            
        except psycopg2.Error as e:
            print(f"❌ Error obteniendo usuarios: {e}")
            if conn:
                conn.close()
            raise Exception("Error al obtener usuarios")
    
    def obtener_por_id(self, usuario_id):
        """Obtener un usuario por ID"""
        conn = self.db.obtener_conexion()
        if not conn:
            raise Exception("Error de conexión a la base de datos")
        
        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(
                '''SELECT id, nombre, apellido, email, edad, telefono, ciudad, 
                          activo, fecha_registro, fecha_actualizacion, genero, 
                          profesion, salario
                   FROM users WHERE id = %s''',
                (usuario_id,)
            )
            usuario = cursor.fetchone()
            conn.close()
            
            if usuario:
                usuario = dict(usuario)
                # Convertir timestamps a string
                if usuario['fecha_registro']:
                    usuario['fecha_registro'] = usuario['fecha_registro'].isoformat()
                if usuario['fecha_actualizacion']:
                    usuario['fecha_actualizacion'] = usuario['fecha_actualizacion'].isoformat()
                return usuario
            else:
                return None
                
        except psycopg2.Error as e:
            print(f"❌ Error obteniendo usuario: {e}")
            if conn:
                conn.close()
            raise Exception("Error al obtener usuario")
    
    def crear(self, datos):
        """Crear nuevo usuario"""
        conn = self.db.obtener_conexion()
        if not conn:
            raise Exception("Error de conexión a la base de datos")
        
        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(
                '''INSERT INTO users (nombre, apellido, email, edad, telefono, ciudad, 
                                      genero, profesion, salario, notas) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                   RETURNING id, nombre, apellido, email, edad, telefono, ciudad, 
                             activo, fecha_registro, fecha_actualizacion, genero, 
                             profesion, salario''',
                (datos.get('nombre'),
                 datos.get('apellido'),
                 datos.get('email'),
                 datos.get('edad'),
                 datos.get('telefono'),
                 datos.get('ciudad'),
                 datos.get('genero'),
                 datos.get('profesion'),
                 datos.get('salario'),
                 datos.get('notas'))
            )
            nuevo_usuario = dict(cursor.fetchone())
            conn.commit()
            conn.close()
            
            # Convertir timestamps a string
            if nuevo_usuario['fecha_registro']:
                nuevo_usuario['fecha_registro'] = nuevo_usuario['fecha_registro'].isoformat()
            if nuevo_usuario['fecha_actualizacion']:
                nuevo_usuario['fecha_actualizacion'] = nuevo_usuario['fecha_actualizacion'].isoformat()
            
            print(f"✅ Usuario creado en PostgreSQL: {nuevo_usuario}")
            return nuevo_usuario
            
        except psycopg2.IntegrityError:
            if conn:
                conn.close()
            raise ValueError("El email ya existe")
        except psycopg2.Error as e:
            print(f"❌ Error creando usuario: {e}")
            if conn:
                conn.close()
            raise Exception("Error al crear usuario")
    
    def actualizar(self, usuario_id, datos):
        """Actualizar usuario completo (PUT)"""
        conn = self.db.obtener_conexion()
        if not conn:
            raise Exception("Error de conexión a la base de datos")
        
        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Construir la consulta dinámicamente
            campos = []
            valores = []
            
            campos_permitidos = ['nombre', 'apellido', 'email', 'edad', 'telefono', 
                               'ciudad', 'genero', 'profesion', 'salario', 'notas', 'activo']
            
            for campo in campos_permitidos:
                if campo in datos:
                    campos.append(f'{campo} = %s')
                    valores.append(datos[campo])
            
            if not campos:
                raise ValueError("No hay campos válidos para actualizar")
            
            # Agregar timestamp de actualización automático (manejado por trigger)
            valores.append(usuario_id)
            
            consulta = f'''
                UPDATE users 
                SET {', '.join(campos)} 
                WHERE id = %s 
                RETURNING id, nombre, apellido, email, edad, telefono, ciudad,
                          activo, fecha_registro, fecha_actualizacion, genero,
                          profesion, salario
            '''
            
            cursor.execute(consulta, valores)
            usuario_actualizado = cursor.fetchone()
            
            if not usuario_actualizado:
                conn.close()
                raise ValueError("Usuario no encontrado")
            
            conn.commit()
            conn.close()
            
            usuario_actualizado = dict(usuario_actualizado)
            # Convertir timestamps a string
            if usuario_actualizado['fecha_registro']:
                usuario_actualizado['fecha_registro'] = usuario_actualizado['fecha_registro'].isoformat()
            if usuario_actualizado['fecha_actualizacion']:
                usuario_actualizado['fecha_actualizacion'] = usuario_actualizado['fecha_actualizacion'].isoformat()
            
            print(f"✅ Usuario actualizado en PostgreSQL: {usuario_actualizado}")
            return usuario_actualizado
            
        except psycopg2.IntegrityError:
            if conn:
                conn.close()
            raise ValueError("El email ya existe")
        except psycopg2.Error as e:
            print(f"❌ Error actualizando usuario: {e}")
            if conn:
                conn.close()
            raise Exception("Error al actualizar usuario")
    
    def actualizar_parcial(self, usuario_id, datos):
        """Actualizar usuario parcial (PATCH)"""
        conn = self.db.obtener_conexion()
        if not conn:
            raise Exception("Error de conexión a la base de datos")
        
        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Verificar que el usuario existe
            cursor.execute('SELECT id FROM users WHERE id = %s', (usuario_id,))
            if not cursor.fetchone():
                conn.close()
                raise ValueError("Usuario no encontrado")
            
            # Construir la consulta dinámicamente solo con campos enviados
            campos = []
            valores = []
            
            campos_permitidos = ['nombre', 'apellido', 'email', 'edad', 'telefono', 
                               'ciudad', 'genero', 'profesion', 'salario', 'notas', 'activo']
            
            # Solo procesar campos que están en el JSON enviado
            for campo in campos_permitidos:
                if campo in datos:
                    campos.append(f'{campo} = %s')
                    valores.append(datos[campo])
            
            if not campos:
                raise ValueError("No hay campos válidos para actualizar")
            
            # El trigger automático maneja fecha_actualizacion
            valores.append(usuario_id)
            
            consulta = f'''
                UPDATE users 
                SET {', '.join(campos)} 
                WHERE id = %s 
                RETURNING id, nombre, apellido, email, edad, telefono, ciudad,
                          activo, fecha_registro, fecha_actualizacion, genero,
                          profesion, salario
            '''
            
            cursor.execute(consulta, valores)
            usuario_actualizado = cursor.fetchone()
            
            conn.commit()
            conn.close()
            
            usuario_actualizado = dict(usuario_actualizado)
            # Convertir timestamps a string
            if usuario_actualizado['fecha_registro']:
                usuario_actualizado['fecha_registro'] = usuario_actualizado['fecha_registro'].isoformat()
            if usuario_actualizado['fecha_actualizacion']:
                usuario_actualizado['fecha_actualizacion'] = usuario_actualizado['fecha_actualizacion'].isoformat()
            
            # Mostrar qué campos se actualizaron
            campos_actualizados = [campo.split(' = ')[0] for campo in campos]
            print(f"✅ Usuario {usuario_id} actualizado (PATCH): {campos_actualizados}")
            
            return {
                "usuario": usuario_actualizado,
                "campos_actualizados": campos_actualizados,
                "mensaje": f"Actualización parcial exitosa de {len(campos_actualizados)} campo(s)"
            }
            
        except psycopg2.IntegrityError:
            if conn:
                conn.close()
            raise ValueError("El email ya existe")
        except psycopg2.Error as e:
            print(f"❌ Error en actualización parcial: {e}")
            if conn:
                conn.close()
            raise Exception("Error al actualizar usuario")
    
    def eliminar(self, usuario_id):
        """Eliminar usuario"""
        conn = self.db.obtener_conexion()
        if not conn:
            raise Exception("Error de conexión a la base de datos")
        
        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Obtener datos del usuario antes de eliminar
            cursor.execute(
                'SELECT nombre, apellido FROM users WHERE id = %s',
                (usuario_id,)
            )
            usuario = cursor.fetchone()
            
            if not usuario:
                conn.close()
                raise ValueError("Usuario no encontrado")
            
            # Eliminar usuario
            cursor.execute('DELETE FROM users WHERE id = %s', (usuario_id,))
            conn.commit()
            conn.close()
            
            nombre_completo = f"{usuario['nombre']} {usuario['apellido'] or ''}".strip()
            print(f"✅ Usuario eliminado de PostgreSQL: {nombre_completo}")
            return {"mensaje": f"Usuario {nombre_completo} eliminado correctamente"}
            
        except psycopg2.Error as e:
            print(f"❌ Error eliminando usuario: {e}")
            if conn:
                conn.close()
            raise Exception("Error al eliminar usuario")
    
    def obtener_estadisticas(self):
        """Obtener estadísticas de usuarios y base de datos"""
        conn = self.db.obtener_conexion()
        if not conn:
            raise Exception("Error de conexión a la base de datos")
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM users')
            total = cursor.fetchone()[0]
            
            cursor.execute('SELECT version()')
            version_pg = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "total_usuarios": total,
                "version_postgresql": version_pg
            }
            
        except psycopg2.Error as e:
            print(f"❌ Error obteniendo información: {e}")
            if conn:
                conn.close()
            raise Exception("Error al obtener información")