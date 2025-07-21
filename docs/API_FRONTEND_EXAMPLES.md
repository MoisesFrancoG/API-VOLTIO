# 💻 API VOLTIO - Ejemplos de Código Frontend

## 🚀 JavaScript Vanilla / Fetch API

### 🔐 Servicio de Autenticación
```javascript
class AuthService {
  constructor(baseUrl = 'http://127.0.0.1:8000/api/v1') {
    this.baseUrl = baseUrl;
    this.token = localStorage.getItem('voltio_token');
  }

  async login(email, password) {
    try {
      const response = await fetch(`${this.baseUrl}/users/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        throw new Error('Credenciales inválidas');
      }

      const data = await response.json();
      this.token = data.access_token;
      localStorage.setItem('voltio_token', this.token);
      return data;
    } catch (error) {
      throw error;
    }
  }

  async register(userData) {
    const response = await fetch(`${this.baseUrl}/users/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    return response.json();
  }

  logout() {
    this.token = null;
    localStorage.removeItem('voltio_token');
  }

  getAuthHeaders() {
    return {
      'Authorization': `Bearer ${this.token}`,
      'Content-Type': 'application/json'
    };
  }

  isAuthenticated() {
    return !!this.token;
  }
}
```

### 🔌 Servicio de Dispositivos
```javascript
class DeviceService {
  constructor(authService) {
    this.auth = authService;
    this.baseUrl = 'http://127.0.0.1:8000/api/v1';
  }

  async getDevices() {
    const response = await fetch(`${this.baseUrl}/devices/`, {
      headers: this.auth.getAuthHeaders()
    });

    if (!response.ok) {
      throw new Error('Error obteniendo dispositivos');
    }

    return response.json();
  }

  async createDevice(deviceData) {
    const response = await fetch(`${this.baseUrl}/devices/`, {
      method: 'POST',
      headers: this.auth.getAuthHeaders(),
      body: JSON.stringify(deviceData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    return response.json();
  }

  async sendRelayCommand(macAddress, action) {
    const response = await fetch(`${this.baseUrl}/devices/${macAddress}/command/relay`, {
      method: 'POST',
      headers: this.auth.getAuthHeaders(),
      body: JSON.stringify({ action })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    return response.json();
  }

  async getDeviceReadings(macAddress, startTime, endTime, limit = 100) {
    const params = new URLSearchParams({
      device_mac: macAddress,
      limit: limit.toString()
    });

    if (startTime) params.append('start_time', startTime);
    if (endTime) params.append('end_time', endTime);

    const response = await fetch(`${this.baseUrl}/lecturas-pzem/?${params}`, {
      headers: this.auth.getAuthHeaders()
    });

    if (!response.ok) {
      throw new Error('Error obteniendo lecturas');
    }

    return response.json();
  }
}
```

### 🔔 Servicio de Notificaciones
```javascript
class NotificationService {
  constructor(authService) {
    this.auth = authService;
    this.baseUrl = 'http://127.0.0.1:8000/api/v1';
  }

  async getNotifications(unreadOnly = false) {
    const params = unreadOnly ? '?unread_only=true' : '';
    const response = await fetch(`${this.baseUrl}/notifications/${params}`, {
      headers: this.auth.getAuthHeaders()
    });

    return response.json();
  }

  async markAsRead(notificationId) {
    const response = await fetch(`${this.baseUrl}/notifications/${notificationId}/read`, {
      method: 'PUT',
      headers: this.auth.getAuthHeaders()
    });

    return response.ok;
  }

  async deleteNotification(notificationId) {
    const response = await fetch(`${this.baseUrl}/notifications/${notificationId}`, {
      method: 'DELETE',
      headers: this.auth.getAuthHeaders()
    });

    return response.ok;
  }
}
```

### 📱 Ejemplo de Uso Completo
```javascript
// Inicializar servicios
const auth = new AuthService();
const deviceService = new DeviceService(auth);
const notificationService = new NotificationService(auth);

// Función de login
async function handleLogin() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  try {
    const result = await auth.login(email, password);
    console.log('Login exitoso:', result.user);
    
    // Cargar dispositivos después del login
    await loadDevices();
  } catch (error) {
    alert('Error de login: ' + error.message);
  }
}

// Cargar dispositivos
async function loadDevices() {
  try {
    const devices = await deviceService.getDevices();
    displayDevices(devices);
  } catch (error) {
    console.error('Error cargando dispositivos:', error);
  }
}

// Controlar relé
async function toggleRelay(macAddress, isOn) {
  try {
    const action = isOn ? 'OFF' : 'ON';
    const result = await deviceService.sendRelayCommand(macAddress, action);
    console.log('Comando enviado:', result);
    
    // Actualizar UI
    updateRelayButton(macAddress, action === 'ON');
  } catch (error) {
    alert('Error enviando comando: ' + error.message);
  }
}

// Crear nuevo dispositivo
async function createDevice() {
  const deviceData = {
    name: document.getElementById('deviceName').value,
    mac_address: document.getElementById('macAddress').value,
    device_type_id: parseInt(document.getElementById('deviceType').value),
    location_id: parseInt(document.getElementById('location').value),
    description: document.getElementById('description').value
  };

  try {
    const device = await deviceService.createDevice(deviceData);
    console.log('Dispositivo creado:', device);
    await loadDevices(); // Recargar lista
  } catch (error) {
    alert('Error creando dispositivo: ' + error.message);
  }
}
```

---

## ⚛️ React Hooks

### 🔐 Hook de Autenticación
```jsx
import { useState, useEffect, createContext, useContext } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('voltio_token'));
  const [loading, setLoading] = useState(true);

  const baseUrl = 'http://127.0.0.1:8000/api/v1';

  useEffect(() => {
    if (token) {
      // Verificar token válido obteniendo info del usuario
      fetchCurrentUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchCurrentUser = async () => {
    try {
      const response = await fetch(`${baseUrl}/users/me`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        // Token inválido
        logout();
      }
    } catch (error) {
      console.error('Error verificando usuario:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    const response = await fetch(`${baseUrl}/users/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      throw new Error('Credenciales inválidas');
    }

    const data = await response.json();
    setToken(data.access_token);
    setUser(data.user);
    localStorage.setItem('voltio_token', data.access_token);
    
    return data;
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('voltio_token');
  };

  const getAuthHeaders = () => ({
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  });

  return (
    <AuthContext.Provider value={{
      user,
      token,
      loading,
      login,
      logout,
      getAuthHeaders,
      isAuthenticated: !!user
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider');
  }
  return context;
};
```

### 🔌 Hook de Dispositivos
```jsx
import { useState, useEffect } from 'react';
import { useAuth } from './useAuth';

export function useDevices() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { getAuthHeaders } = useAuth();

  const baseUrl = 'http://127.0.0.1:8000/api/v1';

  const fetchDevices = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${baseUrl}/devices/`, {
        headers: getAuthHeaders()
      });

      if (!response.ok) {
        throw new Error('Error obteniendo dispositivos');
      }

      const data = await response.json();
      setDevices(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const createDevice = async (deviceData) => {
    const response = await fetch(`${baseUrl}/devices/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(deviceData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    const newDevice = await response.json();
    setDevices(prev => [...prev, newDevice]);
    return newDevice;
  };

  const sendRelayCommand = async (macAddress, action) => {
    const response = await fetch(`${baseUrl}/devices/${macAddress}/command/relay`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ action })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    return response.json();
  };

  const updateDevice = async (deviceId, updateData) => {
    const response = await fetch(`${baseUrl}/devices/${deviceId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(updateData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    const updatedDevice = await response.json();
    setDevices(prev => prev.map(device => 
      device.id === deviceId ? updatedDevice : device
    ));
    return updatedDevice;
  };

  useEffect(() => {
    fetchDevices();
  }, []);

  return {
    devices,
    loading,
    error,
    fetchDevices,
    createDevice,
    sendRelayCommand,
    updateDevice
  };
}
```

### 📱 Componente de Dispositivo
```jsx
import React, { useState } from 'react';
import { useDevices } from './hooks/useDevices';

function DeviceCard({ device }) {
  const [relayState, setRelayState] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { sendRelayCommand } = useDevices();

  const handleRelayToggle = async () => {
    try {
      setIsLoading(true);
      const action = relayState ? 'OFF' : 'ON';
      await sendRelayCommand(device.mac_address, action);
      setRelayState(!relayState);
    } catch (error) {
      alert('Error controlando relé: ' + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="device-card">
      <h3>{device.name}</h3>
      <p>MAC: {device.mac_address}</p>
      <p>Ubicación: {device.location_id}</p>
      
      {device.device_type_id === 5 && ( // NODO_CONTROL_PZEM
        <button 
          onClick={handleRelayToggle}
          disabled={isLoading}
          className={`relay-button ${relayState ? 'on' : 'off'}`}
        >
          {isLoading ? 'Enviando...' : (relayState ? 'Apagar' : 'Encender')}
        </button>
      )}
    </div>
  );
}

function DeviceList() {
  const { devices, loading, error } = useDevices();

  if (loading) return <div>Cargando dispositivos...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="device-list">
      <h2>Mis Dispositivos</h2>
      {devices.map(device => (
        <DeviceCard key={device.id} device={device} />
      ))}
    </div>
  );
}

export default DeviceList;
```

---

## 🌐 Axios (Interceptores)

### 🔧 Configuración de Axios
```javascript
import axios from 'axios';

// Crear instancia de axios
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  timeout: 10000
});

// Interceptor para requests (agregar token)
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('voltio_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para responses (manejar errores)
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('voltio_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### 🔐 Servicio de Autenticación con Axios
```javascript
import api from './axiosConfig';

export const authService = {
  async login(email, password) {
    const response = await api.post('/users/login', { email, password });
    const { access_token, user } = response.data;
    
    localStorage.setItem('voltio_token', access_token);
    return { token: access_token, user };
  },

  async register(userData) {
    const response = await api.post('/users/register', userData);
    return response.data;
  },

  async getCurrentUser() {
    const response = await api.get('/users/me');
    return response.data;
  },

  logout() {
    localStorage.removeItem('voltio_token');
  }
};
```

### 🔌 Servicio de Dispositivos con Axios
```javascript
import api from './axiosConfig';

export const deviceService = {
  async getDevices() {
    const response = await api.get('/devices/');
    return response.data;
  },

  async createDevice(deviceData) {
    const response = await api.post('/devices/', deviceData);
    return response.data;
  },

  async updateDevice(deviceId, updateData) {
    const response = await api.put(`/devices/${deviceId}`, updateData);
    return response.data;
  },

  async deleteDevice(deviceId) {
    await api.delete(`/devices/${deviceId}`);
  },

  async sendRelayCommand(macAddress, action) {
    const response = await api.post(`/devices/${macAddress}/command/relay`, { action });
    return response.data;
  },

  async getDeviceReadings(macAddress, params = {}) {
    const response = await api.get('/lecturas-pzem/', {
      params: { device_mac: macAddress, ...params }
    });
    return response.data;
  }
};
```

---

## 🎨 CSS Styles (Ejemplo)

```css
/* Estilos para componentes de dispositivos */
.device-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.device-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  background: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.device-card h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.device-card p {
  margin: 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}

.relay-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.relay-button.on {
  background: #4CAF50;
  color: white;
}

.relay-button.off {
  background: #f44336;
  color: white;
}

.relay-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.relay-button:hover:not(:disabled) {
  opacity: 0.8;
}

/* Estilos para notificaciones */
.notification {
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
  border-left: 4px solid;
}

.notification.info {
  background: #e3f2fd;
  border-color: #2196f3;
}

.notification.warning {
  background: #fff3e0;
  border-color: #ff9800;
}

.notification.error {
  background: #ffebee;
  border-color: #f44336;
}

.notification.success {
  background: #e8f5e8;
  border-color: #4caf50;
}

.notification.unread {
  font-weight: bold;
}
```

---

## 🔒 Manejo de Errores Avanzado

```javascript
class ApiError extends Error {
  constructor(message, status, details = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.details = details;
  }
}

// Handler de errores personalizado
function handleApiError(error) {
  if (error.response) {
    const { status, data } = error.response;
    
    switch (status) {
      case 400:
        throw new ApiError('Datos inválidos', status, data.detail);
      case 401:
        localStorage.removeItem('voltio_token');
        window.location.href = '/login';
        throw new ApiError('Sesión expirada', status);
      case 403:
        throw new ApiError('Sin permisos para esta acción', status);
      case 404:
        throw new ApiError('Recurso no encontrado', status);
      case 409:
        throw new ApiError('Conflicto: ' + data.detail, status);
      case 422:
        const validationErrors = data.detail.map(err => 
          `${err.loc.join('.')}: ${err.msg}`
        ).join(', ');
        throw new ApiError('Errores de validación: ' + validationErrors, status);
      default:
        throw new ApiError('Error del servidor', status);
    }
  } else if (error.request) {
    throw new ApiError('Sin conexión al servidor', 0);
  } else {
    throw new ApiError('Error inesperado: ' + error.message, 0);
  }
}

// Ejemplo de uso con try-catch
async function createDeviceWithErrorHandling(deviceData) {
  try {
    const device = await deviceService.createDevice(deviceData);
    showSuccessMessage('Dispositivo creado exitosamente');
    return device;
  } catch (error) {
    handleApiError(error);
    showErrorMessage(error.message);
    throw error;
  }
}
```

Esta documentación de código proporciona ejemplos prácticos y listos para usar en diferentes frameworks y situaciones. Los desarrolladores frontend pueden copiar y adaptar estos ejemplos según sus necesidades específicas.
