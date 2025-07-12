"""
Script para ejecutar todas las pruebas de los módulos
"""

import asyncio
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent))

from test_ubicaciones import test_ubicaciones_crud
from test_tipo_sensores import test_tipo_sensores_crud
from test_comandos_ir import test_comandos_ir_crud
from test_alertas import test_alertas_crud
from test_lecturas import test_lecturas_crud

async def run_all_tests():
    """Ejecutar todas las pruebas de los módulos"""
    
    print("🚀 EJECUTANDO TODAS LAS PRUEBAS DE LOS MÓDULOS")
    print("=" * 60)
    
    try:
        # Pruebas de Ubicaciones
        print("\n📍 PRUEBAS DE UBICACIONES")
        await test_ubicaciones_crud()
        
        # Pruebas de Tipo Sensores
        print("\n🔧 PRUEBAS DE TIPO SENSORES")
        await test_tipo_sensores_crud()
        
        # Pruebas de Comandos IR
        print("\n📡 PRUEBAS DE COMANDOS IR")
        await test_comandos_ir_crud()
        
        # Pruebas de Alertas
        print("\n🚨 PRUEBAS DE ALERTAS")
        await test_alertas_crud()
        
        # Pruebas de Lecturas
        print("\n📊 PRUEBAS DE LECTURAS")
        await test_lecturas_crud()
        
        print("\n✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        
    except Exception as e:
        print(f"\n❌ ERROR EN LAS PRUEBAS: {str(e)}")
        sys.exit(1)

def main():
    """Función principal"""
    print("Iniciando suite de pruebas completa...")
    print("Asegúrate de que la API esté corriendo en http://localhost:8000")
    input("Presiona Enter para continuar...")
    
    asyncio.run(run_all_tests())

if __name__ == "__main__":
    main()
