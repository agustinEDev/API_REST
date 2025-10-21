#!/usr/bin/env python3
"""
Pruebas de integración para todo el sistema.

Prueba el funcionamiento completo del sistema incluyendo:
- Integración entre todos los componentes
- Flujos completos de usuario
- Pruebas end-to-end simuladas
- Casos de uso reales

Autor: agustinEDev
Fecha: 21 de octubre de 2025
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import json

# Añadir el directorio raíz al path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import app
from database.connection import DatabaseConnection
from models.user_model import UserModel
from controllers.user_controller import UserController


class TestIntegracionCompleta(unittest.TestCase):
    """Pruebas de integración para todo el sistema."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        self.usuario_completo = {
            'nombre': 'Ana',
            'apellido': 'García',
            'email': 'ana.garcia@email.com',
            'edad': 28,
            'telefono': '+34-600-111-222',
            'ciudad': 'Barcelona',
            'profesion': 'Diseñadora',
            'salario': '35000',
            'genero': 'Femenino'
        }
    
    def tearDown(self):
        """Limpieza después de cada prueba."""
        pass
    
    @patch('database.connection.DatabaseConnection.get_connection')
    def test_flujo_completo_crud_usuario(self, mock_db):
        """Prueba el flujo completo CRUD de un usuario."""
        # Mock de la base de datos
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        # 1. Crear usuario - Mock para INSERT
        mock_cursor.fetchone.return_value = (1,)  # ID del nuevo usuario
        
        with patch('controllers.user_controller.UserController.crear') as mock_crear:
            mock_crear.return_value = ({'exito': True, 'usuario_id': 1}, 201)
            
            response = self.client.post(
                '/usuarios',
                data=json.dumps(self.usuario_completo),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 201)
            data = response.get_json()
            self.assertTrue(data['exito'])
            usuario_id = data['usuario_id']
        
        # 2. Obtener usuario creado - Mock para SELECT
        usuario_creado = {
            'id': usuario_id,
            'nombre': 'Ana',
            'apellido': 'García',
            'email': 'ana.garcia@email.com'
        }
        
        with patch('controllers.user_controller.UserController.obtener_por_id') as mock_obtener:
            mock_obtener.return_value = (
                {'exito': True, 'usuario': usuario_creado}, 200
            )
            
            response = self.client.get(f'/usuarios/{usuario_id}')
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data['exito'])
            self.assertEqual(data['usuario']['nombre'], 'Ana')
        
        # 3. Actualizar usuario - Mock para UPDATE
        datos_actualizacion = self.usuario_completo.copy()
        datos_actualizacion['ciudad'] = 'Madrid'
        
        with patch('controllers.user_controller.UserController.actualizar') as mock_actualizar:
            mock_actualizar.return_value = (
                {'exito': True, 'mensaje': 'Usuario actualizado'}, 200
            )
            
            response = self.client.put(
                f'/usuarios/{usuario_id}',
                data=json.dumps(datos_actualizacion),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data['exito'])
        
        # 4. Actualización parcial con PATCH - Mock para UPDATE parcial
        datos_patch = {'ciudad': 'Valencia', 'salario': '38000'}
        
        with patch('controllers.user_controller.UserController.actualizar_parcial') as mock_patch:
            mock_patch.return_value = (
                {'exito': True, 'mensaje': 'Usuario actualizado parcialmente'}, 200
            )
            
            response = self.client.patch(
                f'/usuarios/{usuario_id}',
                data=json.dumps(datos_patch),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data['exito'])
        
        # 5. Eliminar usuario - Mock para DELETE
        with patch('controllers.user_controller.UserController.eliminar') as mock_eliminar:
            mock_eliminar.return_value = (
                {'exito': True, 'mensaje': 'Usuario eliminado'}, 200
            )
            
            response = self.client.delete(f'/usuarios/{usuario_id}')
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data['exito'])
    
    @patch('database.connection.DatabaseConnection.get_connection')
    def test_flujo_paginacion_usuarios(self, mock_db):
        """Prueba el flujo completo de paginación."""
        # Mock de la base de datos
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        # Crear varios usuarios primero
        usuarios_simulados = []
        for i in range(1, 11):  # 10 usuarios
            usuario = self.usuario_completo.copy()
            usuario['email'] = f'usuario{i}@email.com'
            usuarios_simulados.append(usuario)
        
        # Mock para paginación
        with patch('controllers.user_controller.UserController.obtener_paginados') as mock_paginados:
            # Primera página (usuarios 1-5)
            mock_paginados.return_value = (
                {
                    'exito': True,
                    'usuarios': usuarios_simulados[:5],
                    'pagina_actual': 1,
                    'total_paginas': 2,
                    'total_usuarios': 10
                },
                200
            )
            
            response = self.client.get('/usuarios/paginado?pagina=1&limite=5')
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data['exito'])
            self.assertEqual(len(data['usuarios']), 5)
            self.assertEqual(data['pagina_actual'], 1)
            self.assertEqual(data['total_paginas'], 2)
            
            # Segunda página (usuarios 6-10)
            mock_paginados.return_value = (
                {
                    'exito': True,
                    'usuarios': usuarios_simulados[5:],
                    'pagina_actual': 2,
                    'total_paginas': 2,
                    'total_usuarios': 10
                },
                200
            )
            
            response = self.client.get('/usuarios/paginado?pagina=2&limite=5')
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data['exito'])
            self.assertEqual(len(data['usuarios']), 5)
            self.assertEqual(data['pagina_actual'], 2)
    
    def test_manejo_errores_cadena_completa(self):
        """Prueba el manejo de errores en toda la cadena."""
        # 1. Error de validación de datos
        datos_invalidos = {'nombre': ''}  # Datos incompletos
        
        response = self.client.post(
            '/usuarios',
            data=json.dumps(datos_invalidos),
            content_type='application/json'
        )
        
        self.assertIn(response.status_code, [400])
        data = response.get_json()
        self.assertFalse(data['exito'])
        self.assertIn('error', data)
        
        # 2. Error de ID inválido
        response = self.client.get('/usuarios/abc')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['exito'])
        
        # 3. Error de JSON malformado
        response = self.client.post(
            '/usuarios',
            data='{"json": malformado}',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['exito'])
    
    @patch('database.connection.DatabaseConnection.get_connection')
    def test_integracion_base_datos_modelo_controlador(self, mock_db):
        """Prueba la integración entre base de datos, modelo y controlador."""
        # Mock de la conexión a la base de datos
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        # Instanciar componentes reales
        db_connection = DatabaseConnection()
        user_model = UserModel()
        user_controller = UserController()
        
        # Configurar mocks para simular operaciones de BD
        mock_cursor.fetchall.return_value = [
            (1, 'Ana', 'García', 'ana@email.com', 28, '+34-600-111-222',
             'Barcelona', 'Diseñadora', '35000.00', 'Femenino', True, None, None)
        ]
        mock_cursor.description = [
            ('id',), ('nombre',), ('apellido',), ('email',), ('edad',),
            ('telefono',), ('ciudad',), ('profesion',), ('salario',),
            ('genero',), ('activo',), ('fecha_registro',), ('fecha_actualizacion',)
        ]
        
        # Probar la cadena completa de integración
        with patch.object(user_model, 'db_connection', db_connection):
            with patch.object(user_controller, 'user_model', user_model):
                # El controlador debería usar el modelo, que usa la BD
                resultado, status_code = user_controller.obtener_todos()
                
                self.assertEqual(status_code, 200)
                self.assertIn('usuarios', resultado)
    
    def test_validacion_consistente_en_capas(self):
        """Prueba que la validación sea consistente en todas las capas."""
        datos_con_errores = {
            'nombre': '',  # Nombre vacío
            'email': 'email_invalido',  # Email inválido
            'edad': -5,  # Edad negativa
        }
        
        # La API debería rechazar estos datos
        response = self.client.post(
            '/usuarios',
            data=json.dumps(datos_con_errores),
            content_type='application/json'
        )
        
        # Debería retornar error de validación
        self.assertIn(response.status_code, [400])
        data = response.get_json()
        self.assertFalse(data['exito'])
        self.assertIn('error', data)
    
    def test_formateo_respuestas_consistente(self):
        """Prueba que el formateo de respuestas sea consistente."""
        # Todas las respuestas exitosas deberían tener formato similar
        with patch('controllers.user_controller.UserController.obtener_todos') as mock_obtener:
            mock_obtener.return_value = (
                {
                    'exito': True,
                    'mensaje': 'Usuarios obtenidos exitosamente',
                    'usuarios': []
                },
                200
            )
            
            response = self.client.get('/usuarios')
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            
            # Verificar estructura consistente
            self.assertIn('exito', data)
            self.assertIn('mensaje', data)
            self.assertTrue(data['exito'])
            
        # Todas las respuestas de error deberían tener formato similar
        response = self.client.get('/usuarios/abc')  # ID inválido
        
        data = response.get_json()
        self.assertIn('exito', data)
        self.assertIn('error', data)
        self.assertFalse(data['exito'])


class TestRendimientoYCarga(unittest.TestCase):
    """Pruebas de rendimiento y carga simuladas."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    @patch('controllers.user_controller.UserController.obtener_todos')
    def test_respuesta_multiples_solicitudes(self, mock_controller):
        """Prueba la respuesta a múltiples solicitudes consecutivas."""
        mock_controller.return_value = (
            {'exito': True, 'usuarios': [], 'mensaje': 'OK'}, 200
        )
        
        # Simular múltiples solicitudes consecutivas
        respuestas = []
        for i in range(10):
            response = self.client.get('/usuarios')
            respuestas.append(response)
        
        # Todas las respuestas deberían ser exitosas
        for response in respuestas:
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data['exito'])
    
    def test_manejo_datos_grandes(self):
        """Prueba el manejo de datos grandes (simulado)."""
        # Simular datos grandes en la solicitud
        datos_grandes = {
            'nombre': 'A' * 100,  # Nombre muy largo
            'apellido': 'B' * 100,
            'email': 'email@' + 'x' * 100 + '.com',
            'edad': 25,
            'telefono': '+34-666-777-888',
            'ciudad': 'C' * 100,
            'profesion': 'D' * 100,
            'salario': '45000',
            'genero': 'Masculino'
        }
        
        response = self.client.post(
            '/usuarios',
            data=json.dumps(datos_grandes),
            content_type='application/json'
        )
        
        # Debería manejar los datos grandes apropiadamente
        # (probablemente rechazándolos por validación)
        self.assertIn(response.status_code, [400, 413, 422])


if __name__ == '__main__':
    unittest.main()