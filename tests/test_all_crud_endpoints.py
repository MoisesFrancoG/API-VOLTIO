"""
Pruebas completas de todos los endpoints CRUD de la API Voltio
Incluye todos los módulos: Users, Roles, Locations, DeviceTypes, Devices, DeviceCommands, Notifications
"""
import requests
import json
import time
from typing import Dict, Any


class APITester:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.admin_token = None
        self.user_token = None
        self.test_data = {}

    def log(self, message: str, level: str = "INFO"):
        timestamp = time.strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "ERROR": "❌",
            "WARNING": "⚠️",
            "TEST": "🧪"
        }.get(level, "📝")
        print(f"{timestamp} {prefix} {message}")

    def make_request(self, method: str, endpoint: str, data: dict = None, headers: dict = None, token: str = None):
        """Hacer una petición HTTP con manejo de errores"""
        url = f"{self.base_url}{endpoint}"

        if token:
            if headers is None:
                headers = {}
            headers['Authorization'] = f'Bearer {token}'

        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method.upper() == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")

            return response
        except Exception as e:
            self.log(f"Error en petición {method} {endpoint}: {e}", "ERROR")
            return None

    def setup_authentication(self):
        """Configurar tokens de autenticación"""
        self.log("🔐 Configurando autenticación...", "TEST")

        # Login como SuperAdmin
        admin_creds = {
            "email": "superadmin@voltio.com",
            "password": "SuperAdmin123!"
        }

        response = self.make_request('POST', '/users/login', admin_creds)
        if response and response.status_code == 200:
            self.admin_token = response.json()['access_token']
            self.log("SuperAdmin autenticado correctamente", "SUCCESS")
        else:
            self.log("Error autenticando SuperAdmin", "ERROR")
            return False

        # Crear y autenticar usuario regular
        import random
        unique_id = random.randint(1000, 9999)
        user_data = {
            "username": f"TestUser{unique_id}",
            "email": f"testuser{unique_id}@example.com",
            "password": "testpass123"
        }

        response = self.make_request('POST', '/users/register', user_data)
        if response and response.status_code == 201:
            self.log("Usuario regular creado", "SUCCESS")

            # Login como usuario regular
            user_creds = {
                "email": f"testuser{unique_id}@example.com",
                "password": "testpass123"
            }

            response = self.make_request('POST', '/users/login', user_creds)
            if response and response.status_code == 200:
                self.user_token = response.json()['access_token']
                user_data_response = response.json()
                self.test_data['user_id'] = user_data_response['user_id']
                self.log("Usuario regular autenticado", "SUCCESS")
            else:
                self.log("Error autenticando usuario regular", "ERROR")
        else:
            self.log("Error creando usuario regular", "ERROR")

        return self.admin_token is not None and self.user_token is not None

    def test_users_crud(self):
        """Probar CRUD de Users"""
        self.log("👥 Probando CRUD de Users...", "TEST")

        # GET /users/ - Listar usuarios
        response = self.make_request('GET', '/users/', token=self.admin_token)
        if response and response.status_code == 200:
            users = response.json()
            self.log(
                f"GET /users/ - {len(users)} usuarios encontrados", "SUCCESS")
        else:
            self.log("GET /users/ - Error", "ERROR")

        # POST /users/ - Crear usuario (admin only)
        new_user_data = {
            "username": "AdminCreatedUser",
            "email": "admincreated@example.com",
            "password": "password123",
            "role_id": 2
        }

        response = self.make_request(
            'POST', '/users/', new_user_data, token=self.admin_token)
        if response and response.status_code == 201:
            created_user = response.json()
            self.test_data['created_user_id'] = created_user['id']
            self.log(
                f"POST /users/ - Usuario creado con ID {created_user['id']}", "SUCCESS")
        else:
            self.log("POST /users/ - Error", "ERROR")

        # GET /users/{id} - Obtener usuario por ID
        if 'created_user_id' in self.test_data:
            response = self.make_request(
                'GET', f'/users/{self.test_data["created_user_id"]}', token=self.admin_token)
            if response and response.status_code == 200:
                self.log(
                    f"GET /users/{self.test_data['created_user_id']} - OK", "SUCCESS")
            else:
                self.log(
                    f"GET /users/{self.test_data['created_user_id']} - Error", "ERROR")

        # PUT /users/{id} - Actualizar usuario
        if 'created_user_id' in self.test_data:
            update_data = {
                "username": "AdminCreatedUserUpdated"
            }
            response = self.make_request('PUT', f'/users/{self.test_data["created_user_id"]}',
                                         update_data, token=self.admin_token)
            if response and response.status_code == 200:
                self.log(
                    f"PUT /users/{self.test_data['created_user_id']} - Usuario actualizado", "SUCCESS")
            else:
                self.log(
                    f"PUT /users/{self.test_data['created_user_id']} - Error", "ERROR")

        # GET /users/me - Información del usuario actual
        response = self.make_request('GET', '/users/me', token=self.user_token)
        if response and response.status_code == 200:
            self.log("GET /users/me - OK", "SUCCESS")
        else:
            self.log("GET /users/me - Error", "ERROR")

    def test_roles_crud(self):
        """Probar CRUD de Roles"""
        self.log("🎭 Probando CRUD de Roles...", "TEST")

        # GET /roles/ - Listar roles
        response = self.make_request('GET', '/roles/', token=self.admin_token)
        if response and response.status_code == 200:
            roles = response.json()
            self.log(
                f"GET /roles/ - {len(roles)} roles encontrados", "SUCCESS")
        else:
            self.log("GET /roles/ - Error", "ERROR")

        # POST /roles/ - Crear rol
        new_role_data = {
            "name": "MODERATOR",
            "description": "Moderator role for testing"
        }

        response = self.make_request(
            'POST', '/roles/', new_role_data, token=self.admin_token)
        if response and response.status_code == 201:
            created_role = response.json()
            self.test_data['created_role_id'] = created_role['id']
            self.log(
                f"POST /roles/ - Rol creado con ID {created_role['id']}", "SUCCESS")
        else:
            self.log("POST /roles/ - Error", "ERROR")

        # GET /roles/{id} - Obtener rol por ID
        if 'created_role_id' in self.test_data:
            response = self.make_request(
                'GET', f'/roles/{self.test_data["created_role_id"]}', token=self.admin_token)
            if response and response.status_code == 200:
                self.log(
                    f"GET /roles/{self.test_data['created_role_id']} - OK", "SUCCESS")
            else:
                self.log(
                    f"GET /roles/{self.test_data['created_role_id']} - Error", "ERROR")

        # PUT /roles/{id} - Actualizar rol
        if 'created_role_id' in self.test_data:
            update_data = {
                "name": "MODERATOR_UPDATED",
                "description": "Updated moderator role"
            }
            response = self.make_request('PUT', f'/roles/{self.test_data["created_role_id"]}',
                                         update_data, token=self.admin_token)
            if response and response.status_code == 200:
                self.log(
                    f"PUT /roles/{self.test_data['created_role_id']} - Rol actualizado", "SUCCESS")
            else:
                self.log(
                    f"PUT /roles/{self.test_data['created_role_id']} - Error", "ERROR")

    def test_locations_crud(self):
        """Probar CRUD de Locations"""
        self.log("📍 Probando CRUD de Locations...", "TEST")

        # GET /locations/ - Listar ubicaciones
        response = self.make_request(
            'GET', '/locations/', token=self.user_token)
        if response and response.status_code == 200:
            locations = response.json()
            self.log(
                f"GET /locations/ - {len(locations)} ubicaciones encontradas", "SUCCESS")
        else:
            self.log("GET /locations/ - Error", "ERROR")

        # POST /locations/ - Crear ubicación (admin/moderator only)
        new_location_data = {
            "name": "Test Location",
            "description": "Location for testing",
            "address": "123 Test Street"
        }

        response = self.make_request(
            'POST', '/locations/', new_location_data, token=self.admin_token)
        if response and response.status_code == 201:
            created_location = response.json()
            self.test_data['created_location_id'] = created_location['id']
            self.log(
                f"POST /locations/ - Ubicación creada con ID {created_location['id']}", "SUCCESS")
        else:
            self.log("POST /locations/ - Error", "ERROR")

        # GET /locations/{id} - Obtener ubicación por ID
        if 'created_location_id' in self.test_data:
            response = self.make_request(
                'GET', f'/locations/{self.test_data["created_location_id"]}', token=self.user_token)
            if response and response.status_code == 200:
                self.log(
                    f"GET /locations/{self.test_data['created_location_id']} - OK", "SUCCESS")
            else:
                self.log(
                    f"GET /locations/{self.test_data['created_location_id']} - Error", "ERROR")

        # PUT /locations/{id} - Actualizar ubicación
        if 'created_location_id' in self.test_data:
            update_data = {
                "name": "Test Location Updated",
                "description": "Updated test location"
            }
            response = self.make_request('PUT', f'/locations/{self.test_data["created_location_id"]}',
                                         update_data, token=self.admin_token)
            if response and response.status_code == 200:
                self.log(
                    f"PUT /locations/{self.test_data['created_location_id']} - Ubicación actualizada", "SUCCESS")
            else:
                self.log(
                    f"PUT /locations/{self.test_data['created_location_id']} - Error", "ERROR")

    def test_device_types_crud(self):
        """Probar CRUD de Device Types"""
        self.log("🔧 Probando CRUD de Device Types...", "TEST")

        # GET /device-types/ - Listar tipos de dispositivos
        response = self.make_request(
            'GET', '/device-types/', token=self.user_token)
        if response and response.status_code == 200:
            device_types = response.json()
            self.log(
                f"GET /device-types/ - {len(device_types)} tipos encontrados", "SUCCESS")
        else:
            self.log("GET /device-types/ - Error", "ERROR")

        # POST /device-types/ - Crear tipo de dispositivo
        new_device_type_data = {
            "type_name": "Test Sensor",
            "description": "Test sensor type"
        }

        response = self.make_request(
            'POST', '/device-types/', new_device_type_data, token=self.admin_token)
        if response and response.status_code == 201:
            created_device_type = response.json()
            self.test_data['created_device_type_id'] = created_device_type['id']
            self.log(
                f"POST /device-types/ - Tipo creado con ID {created_device_type['id']}", "SUCCESS")
        else:
            self.log("POST /device-types/ - Error", "ERROR")

        # GET /device-types/{id} - Obtener tipo por ID
        if 'created_device_type_id' in self.test_data:
            response = self.make_request(
                'GET', f'/device-types/{self.test_data["created_device_type_id"]}', token=self.user_token)
            if response and response.status_code == 200:
                self.log(
                    f"GET /device-types/{self.test_data['created_device_type_id']} - OK", "SUCCESS")
            else:
                self.log(
                    f"GET /device-types/{self.test_data['created_device_type_id']} - Error", "ERROR")

        # PUT /device-types/{id} - Actualizar tipo
        if 'created_device_type_id' in self.test_data:
            update_data = {
                "type_name": "Test Sensor Updated",
                "description": "Updated test sensor"
            }
            response = self.make_request('PUT', f'/device-types/{self.test_data["created_device_type_id"]}',
                                         update_data, token=self.admin_token)
            if response and response.status_code == 200:
                self.log(
                    f"PUT /device-types/{self.test_data['created_device_type_id']} - Tipo actualizado", "SUCCESS")
            else:
                self.log(
                    f"PUT /device-types/{self.test_data['created_device_type_id']} - Error", "ERROR")

    def test_devices_crud(self):
        """Probar CRUD de Devices"""
        self.log("📱 Probando CRUD de Devices...", "TEST")

        # Necesitamos IDs válidos para crear un dispositivo
        if 'created_device_type_id' not in self.test_data or 'created_location_id' not in self.test_data:
            self.log("Saltando test de devices - faltan dependencias", "WARNING")
            return

        # GET /devices/ - Listar dispositivos
        response = self.make_request('GET', '/devices/', token=self.user_token)
        if response and response.status_code == 200:
            devices = response.json()
            self.log(
                f"GET /devices/ - {len(devices)} dispositivos encontrados", "SUCCESS")
        else:
            self.log("GET /devices/ - Error", "ERROR")

        # POST /devices/ - Crear dispositivo
        new_device_data = {
            "name": "Test Device",
            "device_type_id": self.test_data['created_device_type_id'],
            "location_id": self.test_data['created_location_id'],
            "mac_address": "AA:BB:CC:DD:EE:FF",
            "description": "Test device for API testing",
            "is_active": True
        }

        response = self.make_request(
            'POST', '/devices/', new_device_data, token=self.user_token)
        if response and response.status_code == 201:
            created_device = response.json()
            self.test_data['created_device_id'] = created_device['id']
            self.log(
                f"POST /devices/ - Dispositivo creado con ID {created_device['id']}", "SUCCESS")
        else:
            self.log("POST /devices/ - Error", "ERROR")

        # GET /devices/{id} - Obtener dispositivo por ID
        if 'created_device_id' in self.test_data:
            response = self.make_request(
                'GET', f'/devices/{self.test_data["created_device_id"]}', token=self.user_token)
            if response and response.status_code == 200:
                self.log(
                    f"GET /devices/{self.test_data['created_device_id']} - OK", "SUCCESS")
            else:
                self.log(
                    f"GET /devices/{self.test_data['created_device_id']} - Error", "ERROR")

        # PUT /devices/{id} - Actualizar dispositivo
        if 'created_device_id' in self.test_data:
            update_data = {
                "name": "Test Device Updated",
                "description": "Updated test device"
            }
            response = self.make_request('PUT', f'/devices/{self.test_data["created_device_id"]}',
                                         update_data, token=self.user_token)
            if response and response.status_code == 200:
                self.log(
                    f"PUT /devices/{self.test_data['created_device_id']} - Dispositivo actualizado", "SUCCESS")
            else:
                self.log(
                    f"PUT /devices/{self.test_data['created_device_id']} - Error", "ERROR")

    def test_device_commands_crud(self):
        """Probar CRUD de Device Commands"""
        self.log("📡 Probando CRUD de Device Commands...", "TEST")

        # Necesitamos un device_id válido
        if 'created_device_id' not in self.test_data:
            self.log(
                "Saltando test de device commands - falta device_id", "WARNING")
            return

        # GET /device-commands/ - Listar comandos
        response = self.make_request(
            'GET', '/device-commands/', token=self.user_token)
        if response and response.status_code == 200:
            commands = response.json()
            self.log(
                f"GET /device-commands/ - {len(commands)} comandos encontrados", "SUCCESS")
        else:
            self.log("GET /device-commands/ - Error", "ERROR")

        # POST /device-commands/ - Crear comando
        new_command_data = {
            "device_id": self.test_data['created_device_id'],
            "command_name": "TEST_COMMAND",
            "ir_code": "0x1234ABCD",
            "description": "Test command for API testing"
        }

        response = self.make_request(
            'POST', '/device-commands/', new_command_data, token=self.admin_token)
        if response and response.status_code == 201:
            created_command = response.json()
            self.test_data['created_command_id'] = created_command['id']
            self.log(
                f"POST /device-commands/ - Comando creado con ID {created_command['id']}", "SUCCESS")
        else:
            self.log("POST /device-commands/ - Error", "ERROR")

        # GET /device-commands/{id} - Obtener comando por ID
        if 'created_command_id' in self.test_data:
            response = self.make_request(
                'GET', f'/device-commands/{self.test_data["created_command_id"]}', token=self.user_token)
            if response and response.status_code == 200:
                self.log(
                    f"GET /device-commands/{self.test_data['created_command_id']} - OK", "SUCCESS")
            else:
                self.log(
                    f"GET /device-commands/{self.test_data['created_command_id']} - Error", "ERROR")

        # PUT /device-commands/{id} - Actualizar comando
        if 'created_command_id' in self.test_data:
            update_data = {
                "command_name": "TEST_COMMAND_UPDATED",
                "description": "Updated test command"
            }
            response = self.make_request('PUT', f'/device-commands/{self.test_data["created_command_id"]}',
                                         update_data, token=self.admin_token)
            if response and response.status_code == 200:
                self.log(
                    f"PUT /device-commands/{self.test_data['created_command_id']} - Comando actualizado", "SUCCESS")
            else:
                self.log(
                    f"PUT /device-commands/{self.test_data['created_command_id']} - Error", "ERROR")

    def test_notifications_crud(self):
        """Probar CRUD de Notifications"""
        self.log("🔔 Probando CRUD de Notifications...", "TEST")

        # GET /notifications/ - Listar notificaciones
        response = self.make_request(
            'GET', '/notifications/', token=self.user_token)
        if response and response.status_code == 200:
            notifications = response.json()
            self.log(
                f"GET /notifications/ - {len(notifications)} notificaciones encontradas", "SUCCESS")
        else:
            self.log("GET /notifications/ - Error", "ERROR")

        # POST /notifications/ - Crear notificación
        new_notification_data = {
            "title": "Test Notification",
            "message": "This is a test notification",
            "type": "info",
            "is_read": False
        }

        response = self.make_request(
            'POST', '/notifications/', new_notification_data, token=self.user_token)
        if response and response.status_code == 201:
            created_notification = response.json()
            self.test_data['created_notification_id'] = created_notification['id']
            self.log(
                f"POST /notifications/ - Notificación creada con ID {created_notification['id']}", "SUCCESS")
        else:
            self.log("POST /notifications/ - Error", "ERROR")

        # GET /notifications/{id} - Obtener notificación por ID
        if 'created_notification_id' in self.test_data:
            response = self.make_request(
                'GET', f'/notifications/{self.test_data["created_notification_id"]}', token=self.user_token)
            if response and response.status_code == 200:
                self.log(
                    f"GET /notifications/{self.test_data['created_notification_id']} - OK", "SUCCESS")
            else:
                self.log(
                    f"GET /notifications/{self.test_data['created_notification_id']} - Error", "ERROR")

        # PUT /notifications/{id} - Actualizar notificación
        if 'created_notification_id' in self.test_data:
            update_data = {
                "title": "Test Notification Updated",
                "is_read": True
            }
            response = self.make_request('PUT', f'/notifications/{self.test_data["created_notification_id"]}',
                                         update_data, token=self.user_token)
            if response and response.status_code == 200:
                self.log(
                    f"PUT /notifications/{self.test_data['created_notification_id']} - Notificación actualizada", "SUCCESS")
            else:
                self.log(
                    f"PUT /notifications/{self.test_data['created_notification_id']} - Error", "ERROR")

    def cleanup_test_data(self):
        """Limpiar datos de prueba"""
        self.log("🧹 Limpiando datos de prueba...", "TEST")

        # Eliminar en orden inverso para respetar foreign keys
        cleanup_items = [
            ('created_notification_id', '/notifications/'),
            ('created_command_id', '/device-commands/'),
            ('created_device_id', '/devices/'),
            ('created_device_type_id', '/device-types/'),
            ('created_location_id', '/locations/'),
            ('created_role_id', '/roles/'),
            ('created_user_id', '/users/')
        ]

        for key, endpoint in cleanup_items:
            if key in self.test_data:
                response = self.make_request(
                    'DELETE', f'{endpoint}{self.test_data[key]}', token=self.admin_token)
                if response and response.status_code in [204, 200]:
                    self.log(
                        f"DELETE {endpoint}{self.test_data[key]} - OK", "SUCCESS")
                else:
                    self.log(
                        f"DELETE {endpoint}{self.test_data[key]} - Error", "ERROR")

        # Eliminar usuario de prueba
        if 'user_id' in self.test_data:
            response = self.make_request(
                'DELETE', f'/users/{self.test_data["user_id"]}', token=self.admin_token)
            if response and response.status_code in [204, 200]:
                self.log(f"Usuario de prueba eliminado", "SUCCESS")
            else:
                self.log(f"Error eliminando usuario de prueba", "ERROR")

    def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        self.log("🚀 Iniciando pruebas completas de la API Voltio...", "TEST")

        # Configurar autenticación
        if not self.setup_authentication():
            self.log("Error en configuración inicial - abortando pruebas", "ERROR")
            return

        # Ejecutar todas las pruebas CRUD
        self.test_users_crud()
        self.test_roles_crud()
        self.test_locations_crud()
        self.test_device_types_crud()
        self.test_devices_crud()
        self.test_device_commands_crud()
        self.test_notifications_crud()

        # Limpiar datos de prueba
        self.cleanup_test_data()

        self.log("🎉 Pruebas completas finalizadas", "TEST")


if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()
