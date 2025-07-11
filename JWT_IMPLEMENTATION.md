# Autenticación JWT - Guía de Implementación

## Resumen

Se ha implementado un sistema de autenticación JWT centralizado que puede ser usado por todas las entidades de la API.

## Estructura implementada

### 1. **Middleware centralizado** (`src/core/auth_middleware.py`)

- `get_current_user()`: Obtiene usuario autenticado del JWT
- `require_roles(roles)`: Factory para requerir roles específicos
- `require_admin()`: Shortcut para requerir solo admin
- `require_admin_or_moderator()`: Shortcut para admin o moderador

### 2. **Servicio de autenticación** (`src/Usuarios/application/auth_service.py`)

- Manejo de tokens JWT (creación, verificación)
- Hash y verificación de contraseñas

### 3. **Esquemas JWT** (`src/Usuarios/domain/schemas.py`)

- `TokenResponse`: Respuesta con token JWT
- `TokenData`: Datos contenidos en el token

## Endpoints implementados

### **Públicos (sin autenticación):**

- `POST /api/v1/usuarios/login` - Login con JWT
- `POST /api/v1/usuarios/register` - Registro público

### **Autenticados (requiere JWT):**

- `GET /api/v1/usuarios/me` - Info del usuario actual
- `GET /api/v1/usuarios/` - Listar usuarios
- `GET /api/v1/roles/` - Listar roles
- `PUT /api/v1/usuarios/{id}` - Actualizar perfil (propio o admin)

### **Solo administradores:**

- `POST /api/v1/usuarios/` - Crear usuario (admin)
- `DELETE /api/v1/usuarios/{id}` - Eliminar usuario
- `DELETE /api/v1/roles/{id}` - Eliminar rol

### **Admin o moderador:**

- `POST /api/v1/roles/` - Crear rol
- `PUT /api/v1/roles/{id}` - Actualizar rol

## Cómo usar en nuevas entidades

### 1. **Endpoint público:**

```python
@router.get("/public-data")
def get_public_data():
    return {"data": "público"}
```

### 2. **Requiere cualquier usuario autenticado:**

```python
from src.core.auth_middleware import get_current_user

@router.get("/protected-data")
def get_protected_data(current_user = Depends(get_current_user)):
    return {"data": f"Hola {current_user.nombre_usuario}"}
```

### 3. **Requiere rol específico:**

```python
from src.core.auth_middleware import require_admin, require_roles

# Solo administradores
@router.delete("/admin-only")
def admin_action(current_user = Depends(require_admin())):
    return {"action": "admin"}

# Múltiples roles
@router.post("/multi-role")
def multi_role_action(current_user = Depends(require_roles([1, 2, 3]))):
    return {"action": "multi-role"}
```

### 4. **Verificación manual en lógica de negocio:**

```python
from src.core.auth_middleware import user_can_modify_resource, user_has_role

def some_use_case(current_user, resource_id):
    if not user_can_modify_resource(current_user, resource_id):
        raise HTTPException(403, "Sin permisos")

    if user_has_role(current_user, [1, 2]):
        # Lógica especial para admin/moderador
        pass
```

## Flujo de autenticación

### 1. **Login:**

```bash
POST /api/v1/usuarios/login
{
  "correo": "user@example.com",
  "contrasena": "password123"
}
```

**Respuesta:**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user_id": 1
}
```

### 2. **Usar token en requests:**

```bash
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## Configuración requerida

### Variables de entorno:

```bash
SECRET_KEY=your-super-secret-jwt-key-256-bits-minimum
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Ventajas del sistema implementado

✅ **Reutilizable**: Un middleware para todas las entidades
✅ **Escalable**: Fácil agregar nuevos niveles de autorización  
✅ **Seguro**: Tokens JWT firmados criptográficamente
✅ **Flexible**: Diferentes permisos por endpoint
✅ **Centralizado**: Mantenimiento en un solo lugar
✅ **Consistente**: Misma lógica en toda la aplicación

## Próximos pasos

1. **Aplicar a todas las entidades existentes**:

   - Sensores, Ubicaciones, TipoSensores, etc.

2. **Configurar roles en base de datos**:

   - 1: Admin
   - 2: Moderador
   - 3: Usuario regular

3. **Implementar refresh tokens** (opcional)
4. **Agregar rate limiting** (opcional)
5. **Logging de eventos de seguridad** (opcional)
