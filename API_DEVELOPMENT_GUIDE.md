# 📋 Guía de Desarrollo Backend - API Endpoints para Sistema Voltio

## 🎯 Información para Desarrollador Backend

### 📊 **Configuració    # Ejemplo: Últimos datos de energía
    query := `from(bucket: "sensores")
        |> range(start: -1h)
        |> filter(fn: (r) => r._measurement == "energy_metrics")
        |> filter(fn: (r) => r.mac == "PZEM-001")
        |> last()`uxDB**
```yaml
Servidor: http://52.201.107.193:8086
Token: lJLzxtHLHvPNgdvU9dcInGYb/qLbLxUPgrePzLd47EKCLUWBzJ+RmJkpH0f1HkmQ
Organización: mi-org
Bucket: sensores
```

---

## 🗄️ **Estructura de Datos en InfluxDB**

### 1️⃣ **Medidores Eléctricos PZEM** - `energy_metrics`

```sql
-- Estructura de la medición
measurement: energy_metrics
tags:
  - deviceId: string (ej: "PZEM-DEV-001")
  - mac: string (ej: "PZEM-001")
  
fields:
  - voltage: float64     -- Voltaje en V (220.5)
  - current: float64     -- Corriente en A (6.82)  
  - power: float64       -- Potencia en W (1504.0)
  - energy: float64      -- Energía acumulada en kWh (1200.45)
  - frequency: float64   -- Frecuencia en Hz (50.2)
  - powerFactor: float64 -- Factor de potencia (0.89)

timestamp: RFC3339
```

**Endpoints Sugeridos:**
```http
GET /api/v1/energy/current?mac={mac}           # Último valor por MAC
GET /api/v1/energy/history?mac={mac}&from={}&to={}  # Histórico
GET /api/v1/energy/consumption?from={}&to={}   # Consumo total período
GET /api/v1/energy/devices                     # Lista de dispositivos
```

### 2️⃣ **Sensores Ambientales DHT22** - `temperature_humidity_metrics`

```sql
-- Estructura de la medición  
measurement: temperature_humidity_metrics
tags:
  - deviceId: string (ej: "DHT22-DEV-001")
  - mac: string (ej: "DHT22-001")

fields:
  - temperature: float64  -- Temperatura en °C (25.8)
  - humidity: float64     -- Humedad en % (65.2)

timestamp: RFC3339
```

**Endpoints Sugeridos:**
```http
GET /api/v1/environment/current?mac={mac}      # Últimas lecturas
GET /api/v1/environment/temperature?from={}&to={}  # Histórico temperatura
GET /api/v1/environment/humidity?from={}&to={}     # Histórico humedad
GET /api/v1/environment/averages?period=hour|day   # Promedios
```

### 3️⃣ **Sensores de Movimiento PIR** - `motion_sensor_metrics`

```sql
-- Estructura de la medición
measurement: motion_sensor_metrics  
tags:
  - mac: string (ej: "PIR-001")

fields:
  - motion_detected: bool  -- Estado movimiento (true/false)

timestamp: RFC3339
```

**Endpoints Sugeridos:**
```http
GET /api/v1/motion/current?mac={mac}           # Estado actual
GET /api/v1/motion/events?mac={mac}&from={}&to={}  # Eventos de movimiento
GET /api/v1/motion/activity?from={}&to={}      # Resumen actividad
GET /api/v1/motion/zones                       # Estado todas las zonas
```

### 4️⃣ **Sensores de Luz** - `light_sensor_metrics`

```sql
-- Estructura de la medición
measurement: light_sensor_metrics
tags:
  - mac: string (ej: "LIGHT-001")

fields:
  - light_level: float64  -- Nivel luz en lux (785.3)

timestamp: RFC3339
```

**Endpoints Sugeridos:**
```http
GET /api/v1/light/current?mac={mac}            # Nivel actual
GET /api/v1/light/history?mac={mac}&from={}&to={}  # Histórico niveles
GET /api/v1/light/averages?period=hour|day     # Promedios
GET /api/v1/light/zones                        # Todos los sensores
```

---

## 📡 **Conexión a InfluxDB**

### **Go (Ejemplo de implementación):**
```go
package main

import (
    "context"
    "fmt"
    "time"
    
    influxdb2 "github.com/influxdata/influxdb-client-go/v2"
    "github.com/influxdata/influxdb-client-go/v2/api"
)

const (
    url    = "http://52.201.107.193:8086"
    token  = "lJLzxtHLHvPNgdvU9dcInGYb/qLbLxUPgrePzLd47EKCLUWBzJ+RmJkpH0f1HkmQ"
    org    = "mi-org"
    bucket = "sensores"
)

func main() {
    client := influxdb2.NewClient(url, token)
    queryAPI := client.QueryAPI(org)
    
    // Ejemplo: Últimos datos de energía
    query := `from(bucket: "sensores")
        |> range(start: -1h)
        |> filter(fn: (r) => r._measurement == "energy_metrics")
        |> filter(fn: (r) => r.mac == "PZEM-001")
        |> last()`
    
    result, err := queryAPI.Query(context.Background(), query)
    if err != nil {
        panic(err)
    }
    
    for result.Next() {
        fmt.Printf("Dispositivo: %s, Campo: %s, Valor: %v, Tiempo: %s\n",
            result.Record().ValueByKey("mac"),
            result.Record().Field(),
            result.Record().Value(),
            result.Record().Time())
    }
    
    client.Close()
}
```

### **Python (Ejemplo alternativo):**
```python
from influxdb_client import InfluxDBClient
from influxdb_client.client.query_api import QueryApi

url = "http://52.201.107.193:8086"
token = "lJLzxtHLHvPNgdvU9dcInGYb/qLbLxUPgrePzLd47EKCLUWBzJ+RmJkpH0f1HkmQ"
org = "mi-org"
bucket = "sensores"

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

# Ejemplo: Datos ambientales última hora
query = f'''
from(bucket: "{bucket}")
    |> range(start: -1h)
    |> filter(fn: (r) => r._measurement == "temperature_humidity_metrics")
    |> filter(fn: (r) => r.mac == "DHT22-001")
'''

result = query_api.query(query)
for table in result:
    for record in table.records:
        print(f"MAC: {record.values.get('mac')}, "
              f"Campo: {record.get_field()}, "
              f"Valor: {record.get_value()}, "
              f"Tiempo: {record.get_time()}")
client.close()
```

---

## 🔍 **Consultas Flux Útiles**

### **Energía - Consumo por período:**
```flux
from(bucket: "sensores")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "energy_metrics")
  |> filter(fn: (r) => r._field == "power")
  |> aggregateWindow(every: 1h, fn: mean)
  |> yield(name: "hourly_power")
```

### **Temperatura - Máximos y mínimos diarios:**
```flux
from(bucket: "sensores")
  |> range(start: -7d)
  |> filter(fn: (r) => r._measurement == "temperature_humidity_metrics")
  |> filter(fn: (r) => r._field == "temperature")
  |> aggregateWindow(every: 1d, fn: max)
  |> yield(name: "daily_max_temp")
```

### **Movimiento - Eventos en rango:**
```flux
from(bucket: "sensores")
  |> range(start: -2h)
  |> filter(fn: (r) => r._measurement == "motion_sensor_metrics")
  |> filter(fn: (r) => r._field == "motion_detected")
  |> filter(fn: (r) => r._value == true)
  |> group(columns: ["mac"])
  |> count()
```

### **Luz - Promedios por zona:**
```flux
from(bucket: "sensores")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "light_sensor_metrics")
  |> filter(fn: (r) => r._field == "light_level")
  |> group(columns: ["mac"])
  |> mean()
  |> yield(name: "average_light_by_zone")
```

---

## 📋 **Modelos de Respuesta JSON Sugeridos**

### **Respuesta Energía:**
```json
{
  "status": "success",
  "data": {
    "deviceId": "PZEM-DEV-001",
    "mac": "PZEM-001",
    "timestamp": "2025-07-23T10:30:00Z",
    "measurements": {
      "voltage": 220.5,
      "current": 6.82,
      "power": 1504.0,
      "energy": 1200.45,
      "frequency": 50.2,
      "powerFactor": 0.89
    }
  }
}
```

### **Respuesta Ambiente:**
```json
{
  "status": "success",
  "data": {
    "deviceId": "DHT22-DEV-001", 
    "mac": "DHT22-001",
    "timestamp": "2025-07-23T10:30:00Z",
    "measurements": {
      "temperature": 25.8,
      "humidity": 65.2
    }
  }
}
```

### **Respuesta Movimiento:**
```json
{
  "status": "success",
  "data": {
    "mac": "PIR-001",
    "timestamp": "2025-07-23T10:30:00Z",
    "motion_detected": true,
    "zone": "Entrada Principal"
  }
}
```

### **Respuesta Luz:**
```json
{
  "status": "success",
  "data": {
    "mac": "LIGHT-001",
    "timestamp": "2025-07-23T10:30:00Z",
    "light_level": 785.3,
    "zone": "Sala"
  }
}
```

---

## 🚀 **Consideraciones para Desarrollo**

### **1. Paginación:**
```http
GET /api/v1/energy/history?mac=PZEM-001&from=2025-07-22T00:00:00Z&to=2025-07-23T00:00:00Z&limit=100&offset=0
```

### **2. Filtros múltiples:**
```http
GET /api/v1/environment/current?macs=DHT22-001,DHT22-002,DHT22-003
```

### **3. Agregaciones:**
```http
GET /api/v1/energy/consumption/summary?period=day&from=2025-07-01&to=2025-07-31
# Respuesta: total, promedio, máximo, mínimo por día
```

### **4. Tiempo real (WebSocket):**
```
ws://tu-api.com/api/v1/realtime?topics=energy,environment,motion,light
```

### **5. Rate Limiting:**
- Implementar límites por IP/API key
- Considerar caché para consultas frecuentes

### **6. Validación:**
- MACs válidas existentes en sistema
- Rangos de fechas razonables
- Parámetros de agregación válidos

---

## 📈 **Métricas de Rendimiento Esperadas**

- **Latencia**: < 100ms para consultas simples
- **Throughput**: 1000+ req/min por endpoint
- **Datos**: ~100MB/día con 20 sensores activos
- **Retención**: Configurar política según necesidades (30d, 90d, 1y)

Esta estructura te permite crear una API REST robusta para consumir todos los datos del sistema IoT Voltio.
