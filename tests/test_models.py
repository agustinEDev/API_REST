#!/usr/bin/env python3
"""
Pruebas unitarias para el modelo de usuarios.

Prueba las funcionalidades del módulo models.user_model incluyendo:
- Operaciones CRUD (Create, Read, Update, Delete)
- Validación de datos
- Manejo de errores
- Formateo de respuestas

Autor: agustinEDev
Fecha: 21 de octubre de 2025
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from datetime import datetime

# Añadir el directorio raíz al path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user_model import UserModel


class TestUserModel(unittest.TestCase):
    """Pruebas para la clase UserModel."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.user_model = UserModel()
        self.usuario_ejemplo = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'email': 'juan@email.com',
            'edad': 25,
            'telefono': '+34-666-777-888',
            'ciudad': 'Madrid',
            'profesion': 'Desarrollador',
            'salario': '45000',
            'genero': 'Masculino'
        }
    
    def tearDown(self):
        """Limpieza después de cada prueba."""
        pass
    
    @patch('models.user_model.UserModel.db_connection')
    def test_obtener_todos_exitoso(self, mock_db):
        """Prueba obtener todos los usuarios exitosamente."""
        # Mock de la conexión y cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.get_connection.return_value = mock_conn
        
        # Datos simulados de la base de datos
        mock_cursor.fetchall.return_value = [
            (1, 'Juan', 'Pérez', 'juan@email.com', 25, '+34-666-777-888', 
             'Madrid', 'Desarrollador', '45000.00', 'Masculino', True,
             datetime.now(), datetime.now())
        ]
        mock_cursor.description = [
            ('id',), ('nombre',), ('apellido',), ('email',), ('edad',),
            ('telefono',), ('ciudad',), ('profesion',), ('salario',),
            ('genero',), ('activo',), ('fecha_registro',), ('fecha_actualizacion',)
        ]
        
        resultado = self.user_model.obtener_todos()
        
        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]['nombre'], 'Juan')
        self.assertEqual(resultado[0]['email'], 'juan@email.com')
    
    @patch('models.user_model.UserModel.db_connection')
    def test_obtener_todos_vacio(self, mock_db):
        """Prueba obtener todos cuando no hay usuarios."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.get_connection.return_value = mock_conn
        mock_cursor.fetchall.return_value = []
        
        resultado = self.user_model.obtener_todos()
        
        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), 0)
    
    @patch('models.user_model.UserModel.db_connection')
    def test_obtener_por_id_existente(self, mock_db):
        """Prueba obtener usuario existente por ID."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.get_connection.return_value = mock_conn
        
        mock_cursor.fetchone.return_value = (
            1, 'Juan', 'Pérez', 'juan@email.com', 25, '+34-666-777-888',
            'Madrid', 'Desarrollador', '45000.00', 'Masculino', True,
            datetime.now(), datetime.now()
        )
        mock_cursor.description = [
            ('id',), ('nombre',), ('apellido',), ('email',), ('edad',),
            ('telefono',), ('ciudad',), ('profesion',), ('salario',),
            ('genero',), ('activo',), ('fecha_registro',), ('fecha_actualizacion',)
        ]
        
        resultado = self.user_model.obtener_por_id(1)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['id'], 1)
        self.assertEqual(resultado['nombre'], 'Juan')
    
    @patch('models.user_model.UserModel.db_connection')
    def test_obtener_por_id_no_existente(self, mock_db):
        """Prueba obtener usuario no existente por ID."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = None
        
        resultado = self.user_model.obtener_por_id(999)
        
        self.assertIsNone(resultado)
    
    @patch('models.user_model.UserModel.db_connection')
    def test_crear_usuario_exitoso(self, mock_db):
        """Prueba crear usuario exitosamente."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = (1,)  # ID del nuevo usuario
        
        resultado = self.user_model.crear(self.usuario_ejemplo)
        
        self.assertEqual(resultado, 1)
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called_once()
    
    @patch('models.user_model.UserModel.db_connection')
    def test_actualizar_usuario_exitoso(self, mock_db):
        """Prueba actualizar usuario exitosamente."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.get_connection.return_value = mock_conn
        mock_cursor.rowcount = 1  # Una fila afectada
        
        resultado = self.user_model.actualizar(1, self.usuario_ejemplo)
        
        self.assertTrue(resultado)
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called_once()
    
    @patch('models.user_model.UserModel.db_connection')
    def test_actualizar_usuario_no_existente(self, mock_db):
        """Prueba actualizar usuario que no existe."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.get_connection.return_value = mock_conn
        mock_cursor.rowcount = 0  # Ninguna fila afectada
        
        resultado = self.user_model.actualizar(999, self.usuario_ejemplo)
        
        self.assertFalse(resultado)
    
    @patch('models.user_model.UserModel.db_connection')
    def test_eliminar_usuario_exitoso(self, mock_db):
        """Prueba eliminar usuario exitosamente."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.get_connection.return_value = mock_conn
        mock_cursor.rowcount = 1  # Una fila afectada
        
        resultado = self.user_model.eliminar(1)
        
        self.assertTrue(resultado)
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called_once()
    
    @patch('models.user_model.UserModel.db_connection')
    def test_eliminar_usuario_no_existente(self, mock_db):
        """Prueba eliminar usuario que no existe."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.get_connection.return_value = mock_conn
        mock_cursor.rowcount = 0  # Ninguna fila afectada
        
        resultado = self.user_model.eliminar(999)
        
        self.assertFalse(resultado)
    
    def test_validar_datos_completos(self):
        """Prueba validación con datos completos y válidos."""
        resultado = self.user_model._validar_datos(self.usuario_ejemplo)
        
        self.assertTrue(resultado['valido'])
        self.assertEqual(len(resultado['errores']), 0)
    
    def test_validar_datos_incompletos(self):
        """Prueba validación con datos incompletos."""
        datos_incompletos = {'nombre': 'Juan'}  # Faltan campos obligatorios
        
        resultado = self.user_model._validar_datos(datos_incompletos)
        
        self.assertFalse(resultado['valido'])
        self.assertGreater(len(resultado['errores']), 0)
    
    def test_validar_email_invalido(self):
        """Prueba validación con email inválido."""
        datos_email_invalido = self.usuario_ejemplo.copy()
        datos_email_invalido['email'] = 'email_invalido'
        
        resultado = self.user_model._validar_datos(datos_email_invalido)
        
        self.assertFalse(resultado['valido'])
        self.assertIn('Email no válido', ' '.join(resultado['errores']))
    
    def test_validar_edad_invalida(self):
        """Prueba validación con edad inválida."""
        datos_edad_invalida = self.usuario_ejemplo.copy()
        datos_edad_invalida['edad'] = -5
        
        resultado = self.user_model._validar_datos(datos_edad_invalida)
        
        self.assertFalse(resultado['valido'])
        self.assertIn('edad', ' '.join(resultado['errores']).lower())
    
    @patch('models.user_model.UserModel.db_connection')
    def test_actualizar_parcial_exitoso(self, mock_db):
        """Prueba actualización parcial de usuario exitosamente."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.get_connection.return_value = mock_conn
        mock_cursor.rowcount = 1  # Una fila afectada
        
        datos_parciales = {'ciudad': 'Valencia', 'salario': '38000'}
        resultado = self.user_model.actualizar_parcial(1, datos_parciales)
        
        self.assertTrue(resultado)
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called_once()
    
    @patch('models.user_model.UserModel.db_connection')
    def test_actualizar_parcial_no_existente(self, mock_db):
        """Prueba actualización parcial de usuario que no existe."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.get_connection.return_value = mock_conn
        mock_cursor.rowcount = 0  # Ninguna fila afectada
        
        datos_parciales = {'ciudad': 'Valencia'}
        resultado = self.user_model.actualizar_parcial(999, datos_parciales)
        
        self.assertFalse(resultado)
    
    @patch('models.user_model.UserModel.db_connection')
    def test_actualizar_parcial_campos_vacios(self, mock_db):
        """Prueba actualización parcial sin campos para actualizar."""
        datos_vacios = {}
        
        resultado = self.user_model.actualizar_parcial(1, datos_vacios)
        
        self.assertFalse(resultado)
    
    @patch('models.user_model.UserModel.db_connection')
    def test_actualizar_parcial_solo_campos_validos(self, mock_db):
        """Prueba actualización parcial filtrando solo campos válidos."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.get_connection.return_value = mock_conn
        mock_cursor.rowcount = 1
        
        datos_mixtos = {
            'ciudad': 'Valencia',  # Campo válido
            'campo_inexistente': 'valor',  # Campo que no debería procesarse
            'salario': '38000'  # Campo válido
        }
        
        resultado = self.user_model.actualizar_parcial(1, datos_mixtos)
        
        self.assertTrue(resultado)
        # Verificar que se llamó execute (el método filtra campos válidos internamente)
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()