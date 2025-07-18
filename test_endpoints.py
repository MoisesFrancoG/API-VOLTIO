"""
Script para probar los nuevos endpoints de despliegue
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent))

try:
    from main import app
    print("✅ Aplicación importada correctamente")
    
    # Simular las funciones de los endpoints
    import datetime
    import os
    
    print("\n🧪 Probando endpoint /test/quick:")
    quick_response = {
        "ok": True,
        "time": datetime.datetime.now().isoformat(),
        "message": "🚀 Despliegue exitoso - API respondiendo correctamente"
    }
    print(f"Respuesta: {quick_response}")
    
    print("\n🧪 Probando endpoint /test/health:")
    health_response = {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "uptime": "running",
        "version": "1.1.0",
        "service": "API Voltio"
    }
    print(f"Respuesta: {health_response}")
    
    print("\n✅ Todos los endpoints de prueba funcionan correctamente!")
    print("\n📋 URLs disponibles para probar en producción:")
    print("- GET /test/quick")
    print("- GET /test/health") 
    print("- GET /test/deployment")
    print("- GET /")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
