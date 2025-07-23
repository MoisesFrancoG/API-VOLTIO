# 🔧 Debug Endpoints - API VOLTIO

## 📋 Endpoints de Debug para Desarrollo

### ¿Por qué necesitas endpoints de debug?

Durante el desarrollo y testing, necesitas obtener **tokens de autenticación rápidamente** para:

- Probar endpoints de la API
- Debugging de aplicaciones frontend
- Automatización de tests
- Validación de integración

---

## 🔐 Endpoints de Debug (Solo Desarrollo)

### ⚠️ **IMPORTANTE**: Estos endpoints solo funcionan en modo desarrollo

Los siguientes endpoints están **deshabilitados en producción** por seguridad.

### 1. 🔑 Obtener Token de SuperAdmin

```http
GET /debug/get-token
```

**¿Cuándo usar?** Para obtener rápidamente un token de SuperAdmin durante desarrollo.

**Respuesta:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "superadmin",
    "email": "superadmin@voltio.com",
    "role_id": 1
  },
  "expires_in_minutes": 30,
  "usage": "Authorization: Bearer <access_token>",
  "warning": "⚠️ Solo para desarrollo - NO usar en producción"
}
```

### 2. 👥 Obtener Tokens de Todos los Usuarios

```http
GET /debug/test-tokens
```

**¿Cuándo usar?** Para obtener tokens de diferentes tipos de usuarios y probar permisos.

**Respuesta:**

```json
{
  "tokens": {
    "superadmin@voltio.com": {
      "access_token": "eyJhbGciOiJIUzI1NiIs...",
      "token_type": "bearer",
      "user": {
        "id": 1,
        "username": "superadmin",
        "email": "superadmin@voltio.com",
        "role_id": 1,
        "role_name": "SuperAdmin"
      }
    },
    "admin@voltio.com": {
      "access_token": "eyJhbGciOiJIUzI1NiIs...",
      "token_type": "bearer",
      "user": {
        "id": 2,
        "username": "admin",
        "email": "admin@voltio.com",
        "role_id": 2,
        "role_name": "Admin"
      }
    }
  },
  "expires_in_minutes": 30,
  "usage": "Authorization: Bearer <access_token>",
  "example_curl": "curl -H 'Authorization: Bearer <token>' https://voltioapi.acstree.xyz/api/v1/users/me",
  "warning": "⚠️ Solo para desarrollo - NO usar en producción"
}
```

---

## 🚀 Scripts de Utilidad

### 1. Script Python para Debug (Solo Desarrollo)

```bash
# Obtener token de SuperAdmin
python get_debug_tokens.py

# Obtener todos los tokens
python get_debug_tokens.py --all

# Probar un token
python get_debug_tokens.py --test "eyJhbGciOiJIUzI1NiIs..."
```

### 2. Script Python para Producción (Via Login)

```bash
# Token de SuperAdmin
python get_tokens.py --user superadmin

# Todos los tokens disponibles
python get_tokens.py --all

# Credenciales personalizadas
python get_tokens.py --custom "mi@email.com" "mipassword"
```

### 3. Script Rápido

```bash
# Obtener token inmediatamente
python get_token_quick.py
```

---

## 🛠️ Integración en Testing

### En Jest/JavaScript

```javascript
// Obtener token para tests
async function getTestToken() {
  const response = await fetch("http://localhost:8000/debug/get-token");
  const data = await response.json();
  return data.access_token;
}

// Usar en tests
beforeAll(async () => {
  const token = await getTestToken();
  global.authHeaders = {
    Authorization: `Bearer ${token}`,
  };
});
```

### En Pytest/Python

```python
import requests

@pytest.fixture(scope="session")
def auth_token():
    """Obtener token de autenticación para tests"""
    response = requests.get("http://localhost:8000/debug/get-token")
    return response.json()["access_token"]

def test_users_endpoint(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get("http://localhost:8000/api/v1/users/", headers=headers)
    assert response.status_code == 200
```

---

## 🔒 Seguridad

### ✅ Protecciones Implementadas

1. **Solo en desarrollo**: Endpoints deshabilitados en producción
2. **Variable de entorno**: Verificación de `environment != "development"`
3. **Error 404**: En producción devuelve "Not Found" para ocultar existencia
4. **Warnings**: Mensajes claros sobre uso solo en desarrollo

### ⚠️ Nunca usar en producción

```python
# ❌ MAL - No hacer esto en producción
if settings.environment == "production":
    # Endpoints de debug habilitados - PELIGROSO
    pass

# ✅ BIEN - Implementación segura
if settings.environment != "development":
    return {"error": "Este endpoint solo está disponible en modo desarrollo"}
```

---

## 💡 Casos de Uso Frecuentes

### 1. Testing Frontend Local

```bash
# Obtener token
python get_debug_tokens.py

# Copiar token y usar en Postman/Insomnia
# o en tu aplicación frontend de desarrollo
```

### 2. Testing Automatizado

```bash
# En script de CI/CD local
TOKEN=$(python get_debug_tokens.py | grep access_token | cut -d'"' -f4)
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/users/
```

### 3. Debugging de API

```bash
# Probar diferentes endpoints rápidamente
python get_debug_tokens.py --all
# Usar tokens para probar permisos por rol
```

---

## 🚀 Ejemplos Completos

### Frontend React/JavaScript

```javascript
// utils/auth.js
export async function getDevToken() {
  if (process.env.NODE_ENV !== "development") {
    throw new Error("Debug tokens only available in development");
  }

  const response = await fetch("/debug/get-token");
  const data = await response.json();

  if (data.error) {
    throw new Error(data.error);
  }

  return data.access_token;
}

// En tu componente
useEffect(() => {
  async function setupAuth() {
    try {
      const token = await getDevToken();
      setAuthToken(token);
    } catch (error) {
      console.error("Error getting debug token:", error);
    }
  }

  setupAuth();
}, []);
```

### Backend Testing

```python
# conftest.py para pytest
import requests
import pytest

@pytest.fixture(scope="session")
def api_client():
    """Cliente de API con autenticación automática"""

    class APIClient:
        def __init__(self):
            self.base_url = "http://localhost:8000"
            self.token = self._get_token()
            self.headers = {"Authorization": f"Bearer {self.token}"}

        def _get_token(self):
            response = requests.get(f"{self.base_url}/debug/get-token")
            return response.json()["access_token"]

        def get(self, endpoint):
            return requests.get(f"{self.base_url}{endpoint}", headers=self.headers)

        def post(self, endpoint, data):
            return requests.post(f"{self.base_url}{endpoint}",
                               json=data, headers=self.headers)

    return APIClient()

# test_users.py
def test_create_user(api_client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Test123!",
        "role_id": 2
    }

    response = api_client.post("/api/v1/users/", user_data)
    assert response.status_code == 201
```

---

## 📞 Soporte

Si tienes problemas con los endpoints de debug:

1. **Verificar ambiente**: Asegúrate de estar en modo desarrollo
2. **Revisar logs**: Comprobar errores en consola del servidor
3. **Validar credenciales**: Usar las credenciales correctas para login
4. **Comprobar red**: Verificar conectividad con la API

---

_🛠️ Herramientas de debug diseñadas para acelerar tu desarrollo_
