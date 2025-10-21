# database/connection.py
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class DatabaseConnection:
    """Clase para manejar la conexión a PostgreSQL"""
    
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'port': os.getenv('DB_PORT')
        }
    
    def validar_configuracion(self):
        """Validar que todas las variables de entorno estén configuradas"""
        variables_requeridas = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_PORT']
        variables_faltantes = []
        
        for var in variables_requeridas:
            if not os.getenv(var):
                variables_faltantes.append(var)
        
        if variables_faltantes:
            print("❌ Error: Faltan las siguientes variables de entorno:")
            for var in variables_faltantes:
                print(f"   - {var}")
            print("\n📋 Asegúrate de que el archivo .env contenga:")
            print("   DB_HOST=localhost")
            print("   DB_NAME=usuarios_app")
            print("   DB_USER=app_user")
            print("   DB_PASSWORD=PruebaDatabase123.")
            print("   DB_PORT=5432")
            return False
        
        return True
    
    def obtener_conexion(self):
        """Obtener conexión a PostgreSQL"""
        try:
            # Verificar que la configuración esté completa
            if not self.validar_configuracion():
                return None
                
            conn = psycopg2.connect(**self.config)
            return conn
        except psycopg2.Error as e:
            print(f"❌ Error conectando a PostgreSQL: {e}")
            return None
    
    def verificar_tabla_existe(self):
        """Verificar que la base de datos y tabla existen"""
        conn = self.obtener_conexion()
        if not conn:
            print("❌ No se pudo conectar a PostgreSQL")
            return False
        
        try:
            cursor = conn.cursor()
            
            # Verificar que la tabla users existe (creada por el script SQL)
            cursor.execute('''
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_name = 'users' AND table_schema = 'public'
                )
            ''')
            tabla_existe = cursor.fetchone()[0]
            
            if not tabla_existe:
                print("❌ La tabla 'users' no existe. Ejecuta primero crear_tabla_users_completo.sql")
                conn.close()
                return False
            
            # Verificar cuántos usuarios hay
            cursor.execute('SELECT COUNT(*) FROM users')
            count = cursor.fetchone()[0]
            
            conn.close()
            print(f"✅ Conexión a PostgreSQL exitosa. Tabla 'users' tiene {count} registros.")
            return True
            
        except psycopg2.Error as e:
            print(f"❌ Error verificando base de datos: {e}")
            if conn:
                conn.close()
            return False
    
    def get_config_info(self):
        """Obtener información de configuración para mostrar"""
        return {
            'host': self.config['host'],
            'database': self.config['database'],
            'user': self.config['user'],
            'port': self.config['port']
        }