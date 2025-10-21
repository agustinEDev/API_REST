#!/usr/bin/env python3
"""
Pruebas unitarias para la conexión a la base de datos.

Prueba las funcionalidades del módulo database.connection incluyendo:
- Validación de configuración
- Conexión a la base de datos
- Verificación de tablas
- Manejo de errores

Autor: agustinEDev
Fecha: 21 de octubre de 2025
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Añadir el directorio raíz al path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection


class TestDatabaseConnection(unittest.TestCase):
    """Pruebas para la clase DatabaseConnection."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.db = DatabaseConnection()
    
    def tearDown(self):
        """Limpieza después de cada prueba."""
        pass
    
    @patch.dict(os.environ, {
        'DB_HOST': 'localhost',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_pass',
        'DB_PORT': '5432'
    })
    def test_validar_configuracion_completa(self):
        """Prueba validación con configuración completa."""
        resultado = self.db.validar_configuracion()
        self.assertTrue(resultado)
    
    @patch.dict(os.environ, {
        'DB_HOST': 'localhost',
        'DB_NAME': 'test_db',
        # Falta DB_USER intencionalmente
        'DB_PASSWORD': 'test_pass',
        'DB_PORT': '5432'
    }, clear=True)
    def test_validar_configuracion_incompleta(self):
        """Prueba validación con configuración incompleta."""
        resultado = self.db.validar_configuracion()
        self.assertFalse(resultado)
    
    @patch.dict(os.environ, {
        'DB_HOST': 'localhost',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_pass',
        'DB_PORT': '5432'
    })
    def test_get_config_info(self):
        """Prueba obtención de información de configuración."""
        # Crear una nueva instancia para que tome las variables de entorno mockeadas
        test_db = DatabaseConnection()
        config = test_db.get_config_info()
        
        self.assertIsInstance(config, dict)
        self.assertIn('host', config)
        self.assertIn('database', config)
        self.assertIn('user', config)
        self.assertIn('port', config)
        self.assertEqual(config['host'], 'localhost')
        self.assertEqual(config['database'], 'test_db')
        self.assertEqual(config['user'], 'test_user')
        self.assertEqual(config['port'], '5432')  # Es string en el config
    
    @patch('database.connection.psycopg2.connect')
    @patch.dict(os.environ, {
        'DB_HOST': 'localhost',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_pass',
        'DB_PORT': '5432'
    })
    def test_get_connection_exitoso(self, mock_connect):
        """Prueba conexión exitosa a la base de datos."""
        # Mock de la conexión
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # Usar el método correcto
        conexion = self.db.obtener_conexion()
        
        self.assertIsNotNone(conexion)
        mock_connect.assert_called_once()
    
    @patch('database.connection.psycopg2.connect')
    @patch.dict(os.environ, {
        'DB_HOST': 'localhost',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_pass',
        'DB_PORT': '5432'
    })
    def test_get_connection_fallo(self, mock_connect):
        """Prueba fallo en la conexión a la base de datos."""
        import psycopg2
        # Mock que simula error de conexión con el tipo correcto
        mock_connect.side_effect = psycopg2.Error("Error de conexión")
        
        # Crear nueva instancia para usar env vars mockeadas
        test_db = DatabaseConnection()
        conexion = test_db.obtener_conexion()
        
        self.assertIsNone(conexion)
    
    @patch('database.connection.DatabaseConnection.obtener_conexion')
    def test_verificar_tabla_existe_exitoso(self, mock_obtener_conexion):
        """Prueba verificación exitosa de existencia de tabla."""
        # Mock de conexión y cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [(True,), (5,)]  # Tabla existe, 5 registros
        mock_obtener_conexion.return_value = mock_conn
        
        resultado = self.db.verificar_tabla_existe()
        
        self.assertTrue(resultado)
        self.assertEqual(mock_cursor.execute.call_count, 2)  # Dos queries
        mock_conn.close.assert_called_once()
    
    @patch('database.connection.DatabaseConnection.obtener_conexion')
    def test_verificar_tabla_no_existe(self, mock_obtener_conexion):
        """Prueba verificación cuando la tabla no existe."""
        # Mock de conexión sin tabla
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (False,)  # Tabla no existe
        mock_obtener_conexion.return_value = mock_conn
        
        resultado = self.db.verificar_tabla_existe()
        
        self.assertFalse(resultado)


if __name__ == '__main__':
    unittest.main()