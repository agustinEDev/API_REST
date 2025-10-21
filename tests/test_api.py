#!/usr/bin/env python3
"""
Pruebas unitarias para la API REST.

Prueba los endpoints de la API Flask incluyendo:
- Todos los endpoints HTTP (GET, POST, PUT, PATCH, DELETE)
- Códigos de respuesta HTTP correctos
- Formato de respuestas JSON
- Manejo de errores y excepciones
- Validación de parámetros

Autor: agustinEDev
Fecha: 21 de octubre de 2025
"""

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Añadir el directorio raíz al path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar la aplicación Flask
from api import app


class TestAPIEndpoints(unittest.TestCase):
    """Pruebas para los endpoints de la API REST."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
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
    
    def test_ruta_raiz(self):
        """Prueba la ruta raíz de la API."""
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('mensaje', data)
        self.assertIn('API REST', data['mensaje'])
    
    @patch('controllers.user_controller.UserController.obtener_todos')
    def test_obtener_usuarios_exitoso(self, mock_controller):
        """Prueba obtener todos los usuarios exitosamente."""
        # Mock del controlador
        mock_controller.return_value = (
            {
                'exito': True,
                'mensaje': 'Usuarios obtenidos exitosamente',
                'usuarios': [
                    {'id': 1, 'nombre': 'Juan', 'email': 'juan@email.com'},
                    {'id': 2, 'nombre': 'María', 'email': 'maria@email.com'}
                ]
            },
            200
        )
        
        response = self.client.get('/usuarios')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['exito'])
        self.assertIn('usuarios', data)
        self.assertEqual(len(data['usuarios']), 2)
    
    @patch('controllers.user_controller.UserController.obtener_todos')
    def test_obtener_usuarios_vacio(self, mock_controller):
        """Prueba obtener usuarios cuando no hay ninguno."""
        mock_controller.return_value = (
            {
                'exito': True,
                'mensaje': 'No hay usuarios registrados',
                'usuarios': []
            },
            200
        )
        
        response = self.client.get('/usuarios')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['exito'])
        self.assertEqual(len(data['usuarios']), 0)
    
    @patch('controllers.user_controller.UserController.obtener_por_id')
    def test_obtener_usuario_por_id_existente(self, mock_controller):
        """Prueba obtener usuario existente por ID."""
        mock_controller.return_value = (
            {
                'exito': True,
                'mensaje': 'Usuario encontrado',
                'usuario': {'id': 1, 'nombre': 'Juan', 'email': 'juan@email.com'}
            },
            200
        )
        
        response = self.client.get('/usuarios/1')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['exito'])
        self.assertIn('usuario', data)
        self.assertEqual(data['usuario']['id'], 1)
    
    @patch('controllers.user_controller.UserController.obtener_por_id')
    def test_obtener_usuario_por_id_no_existente(self, mock_controller):
        """Prueba obtener usuario que no existe."""
        mock_controller.return_value = (
            {
                'exito': False,
                'error': 'Usuario no encontrado'
            },
            404
        )
        
        response = self.client.get('/usuarios/999')
        
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertFalse(data['exito'])
        self.assertIn('error', data)
    
    def test_obtener_usuario_id_invalido(self):
        """Prueba obtener usuario con ID inválido."""
        response = self.client.get('/usuarios/abc')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['exito'])
        self.assertIn('error', data)
    
    @patch('controllers.user_controller.UserController.crear')
    def test_crear_usuario_exitoso(self, mock_controller):
        """Prueba crear usuario exitosamente."""
        mock_controller.return_value = (
            {
                'exito': True,
                'mensaje': 'Usuario creado exitosamente',
                'usuario_id': 1
            },
            201
        )
        
        response = self.client.post(
            '/usuarios',
            data=json.dumps(self.usuario_ejemplo),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertTrue(data['exito'])
        self.assertIn('usuario_id', data)
    
    def test_crear_usuario_sin_datos(self):
        """Prueba crear usuario sin enviar datos."""
        response = self.client.post('/usuarios')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['exito'])
        self.assertIn('error', data)
    
    def test_crear_usuario_json_invalido(self):
        """Prueba crear usuario con JSON inválido."""
        response = self.client.post(
            '/usuarios',
            data='{"json": "inválido"',  # JSON malformado
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['exito'])
        self.assertIn('error', data)
    
    @patch('controllers.user_controller.UserController.actualizar')
    def test_actualizar_usuario_exitoso(self, mock_controller):
        """Prueba actualizar usuario exitosamente."""
        mock_controller.return_value = (
            {
                'exito': True,
                'mensaje': 'Usuario actualizado exitosamente'
            },
            200
        )
        
        response = self.client.put(
            '/usuarios/1',
            data=json.dumps(self.usuario_ejemplo),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['exito'])
    
    @patch('controllers.user_controller.UserController.actualizar')
    def test_actualizar_usuario_no_existente(self, mock_controller):
        """Prueba actualizar usuario que no existe."""
        mock_controller.return_value = (
            {
                'exito': False,
                'error': 'Usuario no encontrado'
            },
            404
        )
        
        response = self.client.put(
            '/usuarios/999',
            data=json.dumps(self.usuario_ejemplo),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertFalse(data['exito'])
    
    def test_actualizar_usuario_id_invalido(self):
        """Prueba actualizar usuario con ID inválido."""
        response = self.client.put(
            '/usuarios/abc',
            data=json.dumps(self.usuario_ejemplo),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['exito'])
    
    @patch('controllers.user_controller.UserController.actualizar_parcial')
    def test_patch_usuario_exitoso(self, mock_controller):
        """Prueba actualización parcial de usuario exitosamente."""
        mock_controller.return_value = (
            {
                'exito': True,
                'mensaje': 'Usuario actualizado parcialmente'
            },
            200
        )
        
        datos_parciales = {
            'ciudad': 'Valencia',
            'salario': '48000'
        }
        
        response = self.client.patch(
            '/usuarios/1',
            data=json.dumps(datos_parciales),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['exito'])
        self.assertEqual(data['mensaje'], 'Usuario actualizado parcialmente')
    
    @patch('controllers.user_controller.UserController.actualizar_parcial')
    def test_patch_usuario_no_existente(self, mock_controller):
        """Prueba actualización parcial de usuario que no existe."""
        mock_controller.return_value = (
            {
                'exito': False,
                'error': 'Usuario no encontrado'
            },
            404
        )
        
        datos_parciales = {'ciudad': 'Valencia'}
        
        response = self.client.patch(
            '/usuarios/999',
            data=json.dumps(datos_parciales),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertFalse(data['exito'])
        self.assertEqual(data['error'], 'Usuario no encontrado')
    
    def test_patch_usuario_id_invalido(self):
        """Prueba actualización parcial con ID inválido."""
        datos_parciales = {'ciudad': 'Valencia'}
        
        response = self.client.patch(
            '/usuarios/abc',
            data=json.dumps(datos_parciales),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['exito'])
        self.assertIn('error', data)
    
    def test_patch_usuario_sin_datos(self):
        """Prueba actualización parcial sin enviar datos."""
        response = self.client.patch('/usuarios/1')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['exito'])
        self.assertIn('error', data)
    
    def test_patch_usuario_json_invalido(self):
        """Prueba actualización parcial con JSON inválido."""
        response = self.client.patch(
            '/usuarios/1',
            data='{"ciudad": "Valencia",}',  # JSON malformado
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['exito'])
        self.assertIn('error', data)
    
    @patch('controllers.user_controller.UserController.actualizar_parcial')
    def test_patch_usuario_datos_invalidos(self, mock_controller):
        """Prueba actualización parcial con datos inválidos."""
        mock_controller.return_value = (
            {
                'exito': False,
                'error': 'Datos de entrada inválidos'
            },
            400
        )
        
        datos_invalidos = {
            'email': 'email_invalido',  # Email sin formato correcto
            'edad': -10  # Edad negativa
        }
        
        response = self.client.patch(
            '/usuarios/1',
            data=json.dumps(datos_invalidos),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['exito'])
        self.assertIn('error', data)
    
    @patch('controllers.user_controller.UserController.actualizar_parcial')
    def test_patch_usuario_campos_vacios(self, mock_controller):
        """Prueba actualización parcial solo con campos vacíos."""
        mock_controller.return_value = (
            {
                'exito': False,
                'error': 'No se proporcionaron campos válidos para actualizar'
            },
            400
        )
        
        datos_vacios = {
            'nombre': '',
            'email': ''
        }
        
        response = self.client.patch(
            '/usuarios/1',
            data=json.dumps(datos_vacios),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['exito'])
        self.assertIn('error', data)
    
    @patch('controllers.user_controller.UserController.eliminar')
    def test_eliminar_usuario_exitoso(self, mock_controller):
        """Prueba eliminar usuario exitosamente."""
        mock_controller.return_value = (
            {
                'exito': True,
                'mensaje': 'Usuario eliminado exitosamente'
            },
            200
        )
        
        response = self.client.delete('/usuarios/1')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['exito'])
    
    @patch('controllers.user_controller.UserController.eliminar')
    def test_eliminar_usuario_no_existente(self, mock_controller):
        """Prueba eliminar usuario que no existe."""
        mock_controller.return_value = (
            {
                'exito': False,
                'error': 'Usuario no encontrado'
            },
            404
        )
        
        response = self.client.delete('/usuarios/999')
        
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertFalse(data['exito'])
    
    def test_eliminar_usuario_id_invalido(self):
        """Prueba eliminar usuario con ID inválido."""
        response = self.client.delete('/usuarios/abc')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['exito'])
    
    @patch('controllers.user_controller.UserController.obtener_paginados')
    def test_obtener_usuarios_paginados_exitoso(self, mock_controller):
        """Prueba obtener usuarios paginados exitosamente."""
        mock_controller.return_value = (
            {
                'exito': True,
                'mensaje': 'Usuarios paginados obtenidos exitosamente',
                'usuarios': [
                    {'id': 1, 'nombre': 'Juan'},
                    {'id': 2, 'nombre': 'María'}
                ],
                'pagina_actual': 1,
                'total_paginas': 5,
                'total_usuarios': 10
            },
            200
        )
        
        response = self.client.get('/usuarios/paginado?pagina=1&limite=2')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['exito'])
        self.assertIn('usuarios', data)
        self.assertIn('pagina_actual', data)
        self.assertIn('total_paginas', data)
    
    def test_obtener_usuarios_paginados_parametros_invalidos(self):
        """Prueba paginación con parámetros inválidos."""
        response = self.client.get('/usuarios/paginado?pagina=abc&limite=xyz')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['exito'])
        self.assertIn('error', data)
    
    def test_metodo_no_permitido(self):
        """Prueba método HTTP no permitido en endpoint que no lo soporta."""
        # Probar un método no implementado en un endpoint específico
        response = self.client.options('/usuarios/1')  # OPTIONS no implementado
        
        self.assertEqual(response.status_code, 405)
    
    def test_ruta_no_encontrada(self):
        """Prueba ruta que no existe."""
        response = self.client.get('/ruta/inexistente')
        
        self.assertEqual(response.status_code, 404)
    
    def test_content_type_incorrecto(self):
        """Prueba solicitud con Content-Type incorrecto."""
        response = self.client.post(
            '/usuarios',
            data=json.dumps(self.usuario_ejemplo),
            content_type='text/plain'  # Content-Type incorrecto
        )
        
        # Debería fallar porque espera application/json
        self.assertIn(response.status_code, [400, 415])
    
    def test_patch_content_type_incorrecto(self):
        """Prueba PATCH con Content-Type incorrecto."""
        datos_parciales = {'ciudad': 'Valencia'}
        
        response = self.client.patch(
            '/usuarios/1',
            data=json.dumps(datos_parciales),
            content_type='text/plain'  # Content-Type incorrecto
        )
        
        # Debería fallar porque espera application/json
        self.assertIn(response.status_code, [400, 415])


class TestAPIErrorHandling(unittest.TestCase):
    """Pruebas para el manejo de errores de la API."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    @patch('controllers.user_controller.UserController.obtener_todos')
    def test_error_interno_servidor(self, mock_controller):
        """Prueba manejo de error interno del servidor."""
        mock_controller.return_value = (
            {
                'exito': False,
                'error': 'Error interno del servidor'
            },
            500
        )
        
        response = self.client.get('/usuarios')
        
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertFalse(data['exito'])
        self.assertIn('error', data)
    
    def test_json_malformado(self):
        """Prueba solicitud con JSON malformado."""
        response = self.client.post(
            '/usuarios',
            data='{"nombre": "Juan", "email":}',  # JSON inválido
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['exito'])
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()