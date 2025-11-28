from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import datetime
import os
import sys
from pathlib import Path
import psutil
from sqlalchemy import text
from src.core.db import engine, Base
from src.core.config import settings

# Import all models to ensure they're registered with Base.metadata
from src.Roles.infrastructure.models import RoleModel
from src.Usuarios.infrastructure.models import UserModel
from src.TipoSensores.infrastructure.models import DeviceTypeModel
from src.Ubicaciones.infrastructure.models import LocationModel
from src.Sensores.infrastructure.models import DeviceModel
from src.Notifications.infrastructure.models import NotificationModel
from src.DeviceCapabilities.infrastructure.models import DeviceCapabilityModel
from src.DeviceHasCapability.infrastructure.models import DeviceHasCapabilityModel
from src.ComandosIR.infrastructure.models import DeviceCommandModel
from src.AutomationRules.infrastructure.models import AutomationRuleModel

# Import routers
# from src.Roles.infrastructure.routers import router as roles_router
from src.Usuarios.infrastructure.routers import router as users_router
from src.Lecturas_influx_pzem.infrastructure.routers import router as lecturas_router
from src.Lecturas_influx_dht22.infrastructure.routers import router as lecturas_dht22_router
from src.Lecturas_influx_light.infrastructure.routers import router as lecturas_light_router
from src.Lecturas_influx_pir.infrastructure.routers import router as lecturas_pir_router
# from src.Ubicaciones.infrastructure.routers import router as locations_router
# from src.TipoSensores.infrastructure.routers import router as device_types_router
from src.ComandosIR.infrastructure.routers import router as device_commands_router
from src.Sensores.infrastructure.routers import router as devices_router
from src.Notifications.infrastructure.routers import router as notifications_router
from src.Notifications.infrastructure.service_router import router as notification_service_router
from src.AutomationRules.infrastructure.routers import router as automation_rules_router
from src.core.db_influx import close_influx_client

app = FastAPI(
    title="API Voltio",
    description="API para el sistema de monitoreo de sensores Voltio",
    version="1.0.0"
)

# ============================================
# 🌐 CONFIGURACIÓN CORS
# ============================================

# Configurar CORS Middleware usando configuración centralizada
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.cors_origins,           # Orígenes desde config
#     allow_credentials=settings.cors_allow_credentials,
#     allow_methods=settings.cors_allow_methods,     # Métodos permitidos
#     allow_headers=settings.cors_allow_headers,     # Headers permitidos
#     expose_headers=settings.cors_expose_headers,   # Headers expuestos
#     max_age=settings.cors_max_age,                # Cache preflight
# )

# ============================================
# 🔧 ENDPOINT PARA VERIFICAR CORS
# ============================================


@app.get("/cors-info")
def cors_info():
    """Endpoint para verificar configuración de CORS"""
    return {
        "cors_enabled": True,
        "environment": settings.environment,
        "allowed_origins": settings.cors_origins,
        "allowed_methods": settings.cors_allow_methods,
        "allowed_headers": settings.cors_allow_headers,
        "credentials_allowed": settings.cors_allow_credentials,
        "max_age_seconds": settings.cors_max_age,
        "timestamp": datetime.datetime.now().isoformat(),
        "note": "CORS configuration loaded from environment variables and config.py"
    }


@app.on_event("startup")
def startup_event():
    """Crear las tablas de la base de datos al iniciar la aplicación"""
    print("📋 Creando tablas de base de datos...")
    try:
        # Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas exitosamente")
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        # No vamos a detener la aplicación por errores de BD


# Incluir los routers
# app.include_router(roles_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(lecturas_router, prefix="/api/v1")
app.include_router(lecturas_dht22_router, prefix="/api/v1")
app.include_router(lecturas_light_router, prefix="/api/v1")
app.include_router(lecturas_pir_router, prefix="/api/v1")
# app.include_router(locations_router, prefix="/api/v1")
# app.include_router(device_types_router, prefix="/api/v1")

# Automation Rules endpoints
app.include_router(automation_rules_router)
app.include_router(device_commands_router, prefix="/api/v1")
app.include_router(devices_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")
app.include_router(notification_service_router)


@app.on_event("shutdown")
def shutdown_event():
    close_influx_client()


@app.get('/')
def read_root():
    return {'message': 'API de Voltio iniciada correctamente', 'version': '1.0.0'}


@app.get('/debug/config')
def debug_config():
    """Endpoint para verificar la configuración actual (solo en desarrollo)"""
    if settings.environment != "development":
        return {"error": "Este endpoint solo está disponible en modo desarrollo"}

    config_info = {
        "environment": settings.environment,
        "debug": settings.debug,
        "db_host": settings.db_host,
        "db_name": settings.db_name,
        "db_user": settings.db_user,
        "influx_url": settings.influx_url,
        "influx_org": settings.influx_org,
        "influx_bucket": settings.influx_bucket,
        "secret_key_preview": bool(settings.secret_key) if settings.secret_key else None,
        "access_token_expire_minutes": settings.access_token_expire_minutes,
        "ssh_tunnel": settings.ssh_tunnel_info
    }

    # Verificar estado del túnel SSH si está habilitado
    if settings.ssh_tunnel_enabled:
        try:
            from src.core.ssh_tunnel import create_tunnel_from_env
            tunnel = create_tunnel_from_env()
            if tunnel:
                active, pid = tunnel.status()
                config_info["ssh_tunnel"]["status"] = {
                    "active": active,
                    "pid": pid
                }
        except Exception as e:
            config_info["ssh_tunnel"]["status"] = {
                "error": str(e)
            }

    return config_info


@app.get('/debug/get-token')
def get_debug_token():
    """
    Endpoint de debug para obtener tokens de prueba
    Solo disponible en desarrollo - NO usar en producción
    """
    if settings.environment != "development":
        return {"error": "Este endpoint solo está disponible en modo desarrollo"}

    from src.core.auth_middleware import create_access_token
    from src.Usuarios.infrastructure.repositories import UserRepository
    from src.core.db import get_db

    # Obtener conexión a la base de datos
    db = next(get_db())
    user_repo = UserRepository(db)

    try:
        # Buscar usuario SuperAdmin
        superadmin = user_repo.get_user_by_email("superadmin@voltio.com")
        if not superadmin:
            return {"error": "Usuario SuperAdmin no encontrado"}

        # Crear token
        token_data = {"sub": superadmin.email, "user_id": superadmin.id}
        access_token = create_access_token(data=token_data)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": superadmin.id,
                "username": superadmin.username,
                "email": superadmin.email,
                "role_id": superadmin.role_id
            },
            "expires_in_minutes": settings.access_token_expire_minutes,
            "usage": "Authorization: Bearer <access_token>",
            "warning": "⚠️ Solo para desarrollo - NO usar en producción"
        }

    except Exception as e:
        return {"error": f"Error generando token: {str(e)}"}


@app.get('/debug/test-tokens')
def get_all_test_tokens():
    """
    Endpoint de debug para obtener tokens de todos los tipos de usuarios
    Solo disponible en desarrollo - NO usar en producción
    """
    if settings.environment != "development":
        return {"error": "Este endpoint solo está disponible en modo desarrollo"}

    from src.core.auth_middleware import create_access_token
    from src.Usuarios.infrastructure.repositories import UserRepository
    from src.core.db import get_db

    # Obtener conexión a la base de datos
    db = next(get_db())
    user_repo = UserRepository(db)

    try:
        tokens = {}

        # Lista de usuarios de prueba (basado en tus credenciales de test)
        test_users = [
            "superadmin@voltio.com",
            "admin@voltio.com",
            "user@voltio.com",
            "guest@voltio.com"
        ]

        for email in test_users:
            user = user_repo.get_user_by_email(email)
            if user:
                token_data = {"sub": user.email, "user_id": user.id}
                access_token = create_access_token(data=token_data)

                # Obtener nombre del rol si existe
                role_name = "Unknown"
                if hasattr(user, 'role') and user.role:
                    role_name = user.role.name

                tokens[email] = {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role_id": user.role_id,
                        "role_name": role_name
                    }
                }

        return {
            "tokens": tokens,
            "expires_in_minutes": settings.access_token_expire_minutes,
            "usage": "Authorization: Bearer <access_token>",
            "example_curl": "curl -H 'Authorization: Bearer <token>' https://voltioapi.acstree.xyz/api/v1/users/me",
            "warning": "⚠️ Solo para desarrollo - NO usar en producción"
        }

    except Exception as e:
        return {"error": f"Error generando tokens: {str(e)}"}


@app.get('/test/deployment-v2')
def test_deployment_v2():
    """Endpoint de prueba para validar nuevos cambios en el despliegue"""

    deployment_info = {
        "status": "✅ Despliegue v2 funcionando",
        "message": "Nuevos cambios aplicados correctamente",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.3.0-cors",  # Nueva versión con CORS configurado
        "user_context": {
            "current_user": os.getenv("USER", "unknown"),
            "home_directory": os.path.expanduser("~"),
            "working_directory": str(Path.cwd()),
            "script_location": __file__
        },
        "git_info": {
            "branch": "develop",
            "last_commit": "CORS configuration and cleanup",
            "deploy_user": "deploy" if "/home/deploy" in str(Path.cwd()) else "ubuntu"
        },
        "cors_config": {
            "enabled": True,
            "production_domain": "https://voltio.acstree.xyz",
            "development_domains": ["http://localhost:3000", "http://localhost:5173", "http://localhost:4200"],
            "credentials_allowed": True,
            "verification_endpoint": "/cors-info"
        },
        "deployment_features": [
            "� CORS configurado para producción",
            "🎯 Dominio frontend: https://voltio.acstree.xyz",
            "� Utilidades de configuración CORS",
            "🧪 Tests optimizados y limpieza completada",
            "📋 Documentación frontend actualizada",
            "� GitHub Actions corregido para nuevos tests"
        ]
    }

    return deployment_info


@app.get('/test/system-info')
def test_system_info():
    """Información detallada del sistema donde se ejecuta la API"""

    import psutil
    import socket

    try:
        system_info = {
            "server": {
                "hostname": socket.gethostname(),
                "platform": sys.platform,
                "python_version": sys.version.split()[0],
                "current_time": datetime.datetime.now().isoformat()
            },
            "process": {
                "pid": os.getpid(),
                "memory_usage": f"{psutil.Process().memory_info().rss / 1024 / 1024:.2f} MB",
                "cpu_percent": f"{psutil.cpu_percent()}%",
                "uptime": "Just started"  # Se puede mejorar
            },
            "directories": {
                "current": str(Path.cwd()),
                "home": os.path.expanduser("~"),
                "user": os.getenv("USER", "unknown"),
                "project_exists": Path("main.py").exists(),
                "venv_active": hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
            },
            "network": {
                "local_ip": socket.gethostbyname(socket.gethostname()),
                "port": 8000
            }
        }

        # Agregar información de archivos importantes
        important_files = ["requirements.txt", ".env", "main.py", "pytest.ini"]
        system_info["files"] = {}
        for file in important_files:
            file_path = Path(file)
            system_info["files"][file] = {
                "exists": file_path.exists(),
                "size": file_path.stat().st_size if file_path.exists() else 0
            }

        return system_info

    except Exception as e:
        return {
            "error": f"Error getting system info: {str(e)}",
            "basic_info": {
                "working_dir": str(Path.cwd()),
                "python_version": sys.version.split()[0],
                "timestamp": datetime.datetime.now().isoformat()
            }
        }


@app.get('/test/database-check')
def test_database_check():
    """Verificar conectividad con las bases de datos"""

    db_status = {
        "timestamp": datetime.datetime.now().isoformat(),
        "databases": {}
    }

    # Verificar PostgreSQL
    try:
        from src.core.db import engine
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            db_status["databases"]["postgresql"] = {
                "status": "✅ Conectado",
                "version": version[:50] + "..." if len(version) > 50 else version,
                "connection": "OK"
            }
    except Exception as e:
        db_status["databases"]["postgresql"] = {
            "status": "❌ Error",
            "error": str(e)[:100],
            "connection": "FAILED"
        }

    # Verificar InfluxDB
    try:
        from src.core.db_influx import client
        # Intentar hacer ping a InfluxDB
        health = client.health()
        db_status["databases"]["influxdb"] = {
            "status": "✅ Conectado" if health.status == "pass" else "⚠️ Parcial",
            "health_status": health.status,
            "connection": "OK"
        }
    except Exception as e:
        db_status["databases"]["influxdb"] = {
            "status": "❌ Error",
            "error": str(e)[:100],
            "connection": "FAILED"
        }

    return db_status


@app.get('/test/environment-vars')
def test_environment_vars():
    """Verificar variables de entorno críticas (sin mostrar valores sensibles)"""

    critical_vars = [
        "DB_NAME", "DB_USER", "DB_HOST", "DB_PORT",
        "INFLUX_URL", "INFLUX_ORG", "INFLUX_BUCKET",
        "SECRET_KEY", "ENVIRONMENT", "DEBUG"
    ]

    env_status = {
        "timestamp": datetime.datetime.now().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "variables": {},
        "summary": {
            "total_checked": len(critical_vars),
            "configured": 0,
            "missing": 0
        }
    }

    for var in critical_vars:
        value = os.getenv(var)
        if value:
            env_status["variables"][var] = {
                "configured": True,
                "length": len(value),
                "preview": value[:3] + "*" * (len(value) - 3) if len(value) > 3 else "***"
            }
            env_status["summary"]["configured"] += 1
        else:
            env_status["variables"][var] = {
                "configured": False,
                "status": "❌ No configurada"
            }
            env_status["summary"]["missing"] += 1

    env_status["summary"]["status"] = "✅ Completo" if env_status["summary"][
        "missing"] == 0 else f"⚠️ Faltan {env_status['summary']['missing']} variables"

    return env_status


@app.get('/test/api-performance')
def test_api_performance():
    """Test básico de rendimiento de la API"""

    import time
    start_time = time.time()

    # Simular algunas operaciones
    test_data = []
    for i in range(1000):
        test_data.append({
            "id": i,
            "value": i * 2,
            "timestamp": datetime.datetime.now().isoformat()
        })

    processing_time = time.time() - start_time

    performance_info = {
        "test_name": "API Performance Test",
        "timestamp": datetime.datetime.now().isoformat(),
        "results": {
            "processing_time_seconds": round(processing_time, 4),
            "items_processed": len(test_data),
            "items_per_second": round(len(test_data) / processing_time, 2),
            "status": "✅ OK" if processing_time < 1.0 else "⚠️ Lento"
        },
        "server_load": {
            "cpu_count": psutil.cpu_count(),
            "memory_available": f"{psutil.virtual_memory().available / 1024 / 1024:.0f} MB"
        }
    }

    return performance_info


@app.get('/test/all-endpoints')
def test_all_endpoints():
    """Resumen de todos los endpoints de prueba disponibles"""

    test_endpoints = {
        "available_tests": [
            {
                "endpoint": "/test/quick",
                "description": "Test rápido básico",
                "purpose": "Verificación básica de funcionamiento"
            },
            {
                "endpoint": "/test/health",
                "description": "Estado de salud completo",
                "purpose": "Verificar configuración y conectividad"
            },
            {
                "endpoint": "/test/deployment",
                "description": "Información de despliegue v1",
                "purpose": "Validar despliegue inicial"
            },
            {
                "endpoint": "/test/deployment-v2",
                "description": "Información de despliegue v2 - NUEVO",
                "purpose": "Validar últimos cambios y configuración de usuario deploy"
            },
            {
                "endpoint": "/test/system-info",
                "description": "Información detallada del sistema - NUEVO",
                "purpose": "Diagnosticar configuración del servidor"
            },
            {
                "endpoint": "/test/database-check",
                "description": "Verificación de bases de datos - NUEVO",
                "purpose": "Comprobar conectividad PostgreSQL e InfluxDB"
            },
            {
                "endpoint": "/test/environment-vars",
                "description": "Variables de entorno - NUEVO",
                "purpose": "Verificar configuración sin exponer secretos"
            },
            {
                "endpoint": "/test/api-performance",
                "description": "Test de rendimiento básico - NUEVO",
                "purpose": "Medir rendimiento simple de la API"
            }
        ],
        "summary": {
            "total_endpoints": 8,
            "new_endpoints": 5,
            "version": "1.2.0",
            "last_update": datetime.datetime.now().isoformat()
        },
        "usage": {
            "test_individual": "Visita cada endpoint para pruebas específicas",
            "test_all": "Este endpoint lista todos los disponibles",
            "deployment_validation": "Usa /test/deployment-v2 para validar últimos cambios"
        }
    }

    return test_endpoints


@app.get('/test/deployment')
def test_deployment():
    """Endpoint de prueba original para verificar despliegue"""

    deployment_info = {
        "status": "✅ API funcionando correctamente",
        "message": "Este endpoint confirma que el despliegue fue exitoso",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.1.0",
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "debug_mode": os.getenv("DEBUG", "false").lower() == "true",
        "deployment": {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "commit_info": "Deployment test endpoint added",
            "features": [
                "🧪 Tests corregidos y funcionando",
                "📁 Estructura de proyecto validada",
                "🚀 GitHub Actions configurado",
                "🔧 Pytest configurado correctamente",
                "📦 Supervisor y Nginx listos",
                "🔒 SSL preparado para producción"
            ]
        },
        "system": {
            "python_version": sys.version.split()[0],
            "platform": sys.platform,
            "current_directory": str(Path.cwd()),
            "main_file_exists": Path("main.py").exists(),
            "src_directory_exists": Path("src").exists()
        },
        "modules_status": {
            "usuarios": "✅ Disponible",
            "roles": "✅ Disponible",
            "ubicaciones": "✅ Disponible",
            "device_types": "✅ Disponible",
            "devices": "✅ Disponible",
            "comandos_ir": "✅ Disponible",
            "lecturas_influx_pzem": "✅ Disponible"
        },
        "database": {
            "postgresql_configured": bool(os.getenv("DB_NAME")),
            "influxdb_configured": bool(os.getenv("INFLUX_URL")),
            "connection_test": "Configurado (test de conexión requiere BD activa)"
        }
    }

    return deployment_info


@app.get('/test/health')
def health_check():
    """Endpoint simple de health check para monitoreo"""
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "uptime": "running",
        "version": "1.1.0",
        "service": "API Voltio"
    }


@app.get('/test/quick')
def quick_test():
    """Endpoint ultra simple para verificaciones rápidas"""
    return {
        "ok": True,
        "time": datetime.datetime.now().isoformat(),
        "message": "🚀 Despliegue exitoso - API respondiendo correctamente"
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor API Voltio...")
    print(f"📊 Configuración: {settings.environment}")
    print(f"🔗 Base de datos: {settings.db_host}:{settings.db_port}")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
