#!/usr/bin/env python3
"""
Cliente de pruebas para API REST de Usuarios.

Este módulo proporciona una interfaz de línea de comandos para interactuar
con la API REST de usuarios, permitiendo realizar operaciones CRUD completas.

Autor: Tu nombre
Fecha: 21 de octubre de 2025
"""

import json
import sys
from typing import Dict, Any, Optional
import requests
from requests.exceptions import ConnectionError, RequestException, Timeout


class APIClient:
    """Cliente para interactuar con la API REST de usuarios."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Inicializa el cliente API.
        
        Args:
            base_url: URL base de la API
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = 10
        
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Realiza una petición HTTP a la API.
        
        Args:
            method: Método HTTP (GET, POST, PUT, PATCH, DELETE)
            endpoint: Endpoint de la API
            data: Datos a enviar en la petición
            
        Returns:
            Respuesta de la API como diccionario
            
        Raises:
            ConnectionError: Si no se puede conectar con la API
            RequestException: Si hay un error en la petición
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            
            # Verificar si la respuesta es exitosa
            response.raise_for_status()
            
            return response.json()
            
        except ConnectionError:
            raise ConnectionError(f"❌ No se pudo conectar con la API en {self.base_url}")
        except Timeout:
            raise Timeout(f"⏰ Timeout al conectar con la API (>{self.timeout}s)")
        except RequestException as e:
            if hasattr(e.response, 'json'):
                try:
                    error_data = e.response.json()
                    raise RequestException(f"❌ Error API: {error_data.get('error', str(e))}")
                except:
                    pass
            raise RequestException(f"❌ Error en la petición: {e}")

    def get_all_users(self) -> Dict[str, Any]:
        """Obtiene todos los usuarios."""
        return self._make_request('GET', '/usuarios')

    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """Obtiene un usuario por su ID."""
        return self._make_request('GET', f'/usuarios/{user_id}')

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo usuario."""
        return self._make_request('POST', '/usuarios', user_data)

    def update_user_complete(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza completamente un usuario."""
        return self._make_request('PUT', f'/usuarios/{user_id}', user_data)

    def update_user_partial(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza parcialmente un usuario."""
        return self._make_request('PATCH', f'/usuarios/{user_id}', user_data)

    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Elimina un usuario."""
        return self._make_request('DELETE', f'/usuarios/{user_id}')


class MenuPeticiones:
    """Interfaz de menú para realizar peticiones a la API."""
    
    def __init__(self):
        """Inicializa el menú con el cliente API."""
        self.api_client = APIClient()
        self.opciones = {
            '1': ('Obtener todos los usuarios', self.obtener_todos_usuarios),
            '2': ('Obtener usuario por ID', self.obtener_usuario_por_id),
            '3': ('Crear nuevo usuario', self.crear_nuevo_usuario),
            '4': ('Actualizar usuario completo', self.actualizar_usuario_completo),
            '5': ('Actualizar usuario parcialmente', self.actualizar_usuario_parcialmente),
            '6': ('Eliminar usuario', self.eliminar_usuario),
            '7': ('Salir', self._salir)
        }

    def mostrar_menu(self) -> None:
        """Muestra el menú de opciones."""
        print("\n" + "="*50)
        print("🌐 CLIENTE API REST - GESTIÓN DE USUARIOS")
        print("="*50)
        
        for opcion, (descripcion, _) in self.opciones.items():
            print(f"{opcion}. {descripcion}")
        
        print("="*50)

    def ejecutar_opcion(self, opcion: str) -> bool:
        """
        Ejecuta la opción seleccionada.
        
        Args:
            opcion: Opción seleccionada por el usuario
            
        Returns:
            False si el usuario quiere salir, True en caso contrario
        """
        if opcion in self.opciones:
            descripcion, funcion = self.opciones[opcion]
            print(f"\n🔄 Ejecutando: {descripcion}")
            
            try:
                resultado = funcion()
                if opcion == '7':  # Opción salir
                    return False
                    
            except (ConnectionError, RequestException, Timeout) as e:
                print(f"❌ Error: {e}")
                
        else:
            print("❌ Opción no válida. Por favor, seleccione una opción del 1 al 7.")
            
        return True

    def _imprimir_respuesta(self, respuesta: Dict[str, Any]) -> None:
        """Imprime la respuesta de la API de forma legible."""
        print("\n📋 Respuesta de la API:")
        print("-" * 30)
        print(json.dumps(respuesta, indent=2, ensure_ascii=False))
        print("-" * 30)

    def _solicitar_entero(self, mensaje: str) -> int:
        """
        Solicita un número entero al usuario con validación.
        
        Args:
            mensaje: Mensaje a mostrar al usuario
            
        Returns:
            Número entero ingresado por el usuario
        """
        while True:
            try:
                valor = input(f"📝 {mensaje}: ").strip()
                return int(valor)
            except ValueError:
                print("❌ Por favor ingrese un número válido.")

    def _solicitar_texto(self, mensaje: str, obligatorio: bool = True) -> str:
        """
        Solicita texto al usuario con validación.
        
        Args:
            mensaje: Mensaje a mostrar al usuario
            obligatorio: Si el campo es obligatorio
            
        Returns:
            Texto ingresado por el usuario
        """
        while True:
            valor = input(f"📝 {mensaje}: ").strip()
            if valor or not obligatorio:
                return valor
            print("❌ Este campo es obligatorio.")

    def obtener_todos_usuarios(self) -> None:
        """Obtiene y muestra todos los usuarios."""
        respuesta = self.api_client.get_all_users()
        self._imprimir_respuesta(respuesta)

    def obtener_usuario_por_id(self) -> None:
        """Obtiene y muestra un usuario por su ID."""
        usuario_id = self._solicitar_entero("Ingrese el ID del usuario")
        respuesta = self.api_client.get_user_by_id(usuario_id)
        self._imprimir_respuesta(respuesta)

    def crear_nuevo_usuario(self) -> None:
        """Crea un nuevo usuario solicitando los datos necesarios."""
        print("\n📝 Creando nuevo usuario:")
        
        data = {
            'nombre': self._solicitar_texto("Ingrese el nombre del usuario"),
            'apellido': self._solicitar_texto("Ingrese el apellido del usuario"),
            'email': self._solicitar_texto("Ingrese el email del usuario"),
            'edad': self._solicitar_entero("Ingrese la edad del usuario")
        }
        
        # Campos opcionales
        telefono = self._solicitar_texto("Ingrese el teléfono (opcional)", obligatorio=False)
        if telefono:
            data['telefono'] = telefono
            
        ciudad = self._solicitar_texto("Ingrese la ciudad (opcional)", obligatorio=False)
        if ciudad:
            data['ciudad'] = ciudad
        
        respuesta = self.api_client.create_user(data)
        self._imprimir_respuesta(respuesta)

    def actualizar_usuario_completo(self) -> None:
        """Actualiza completamente un usuario."""
        usuario_id = self._solicitar_entero("Ingrese el ID del usuario a actualizar")
        
        print("\n📝 Actualizando usuario completo:")
        data = {
            'nombre': self._solicitar_texto("Ingrese el nuevo nombre"),
            'apellido': self._solicitar_texto("Ingrese el nuevo apellido"),
            'email': self._solicitar_texto("Ingrese el nuevo email"),
            'edad': self._solicitar_entero("Ingrese la nueva edad")
        }
        
        respuesta = self.api_client.update_user_complete(usuario_id, data)
        self._imprimir_respuesta(respuesta)

    def actualizar_usuario_parcialmente(self) -> None:
        """Actualiza parcialmente un usuario."""
        usuario_id = self._solicitar_entero("Ingrese el ID del usuario a actualizar")
        
        print("\n📝 Actualización parcial (deje en blanco los campos que no desea cambiar):")
        
        data = {}
        campos_disponibles = [
            ('nombre', 'nombre'),
            ('apellido', 'apellido'), 
            ('email', 'email'),
            ('edad', 'edad'),
            ('telefono', 'teléfono'),
            ('ciudad', 'ciudad'),
            ('profesion', 'profesión'),
            ('salario', 'salario')
        ]
        
        for campo, descripcion in campos_disponibles:
            if campo in ['edad', 'salario']:
                valor = input(f"📝 Nuevo {descripcion} (opcional): ").strip()
                if valor:
                    try:
                        data[campo] = int(valor) if campo == 'edad' else valor
                    except ValueError:
                        print(f"❌ Valor inválido para {descripcion}, se omitirá.")
            else:
                valor = self._solicitar_texto(f"Nuevo {descripcion} (opcional)", obligatorio=False)
                if valor:
                    data[campo] = valor
        
        if not data:
            print("❌ No se proporcionaron campos para actualizar.")
            return
            
        respuesta = self.api_client.update_user_partial(usuario_id, data)
        self._imprimir_respuesta(respuesta)

    def eliminar_usuario(self) -> None:
        """Elimina un usuario previa confirmación."""
        usuario_id = self._solicitar_entero("Ingrese el ID del usuario a eliminar")
        
        confirmacion = input(f"⚠️  ¿Está seguro de eliminar el usuario {usuario_id}? (s/N): ").strip().lower()
        
        if confirmacion in ['s', 'si', 'sí', 'y', 'yes']:
            respuesta = self.api_client.delete_user(usuario_id)
            self._imprimir_respuesta(respuesta)
        else:
            print("❌ Operación cancelada.")

    def _salir(self) -> None:
        """Termina la aplicación."""
        print("\n👋 ¡Gracias por usar el cliente API REST!")
        print("🔄 Cerrando aplicación...")

    def run(self) -> None:
        """Ejecuta el bucle principal del menú."""
        print("🚀 Iniciando cliente API REST...")
        
        # Verificar conexión con la API
        try:
            self.api_client._make_request('GET', '/')
            print("✅ Conexión con la API establecida correctamente.")
        except (ConnectionError, RequestException, Timeout) as e:
            print(f"❌ No se pudo conectar con la API: {e}")
            print("💡 Asegúrese de que el servidor Flask esté ejecutándose.")
            return
        
        # Bucle principal
        while True:
            self.mostrar_menu()
            opcion = input("\n🎯 Seleccione una opción: ").strip()
            
            if not self.ejecutar_opcion(opcion):
                break
            
            input("\n⏸️  Presione Enter para continuar...")


def main() -> None:
    """Función principal del programa."""
    try:
        menu = MenuPeticiones()
        menu.run()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()