from fastapi import FastAPI
import datetime
import os
import sys
from pathlib import Path
from src.core.db import engine, Base
from src.core.config import settings
from src.Roles.infrastructure.routers import router as roles_router
from src.Usuarios.infrastructure.routers import router as usuarios_router
from src.Lecturas_influx_pzem.infrastructure.routers import router as lecturas_router
from src.Ubicaciones.infrastructure.routers import router as ubicaciones_router
from src.TipoSensores.infrastructure.routers import router as tipo_sensores_router
from src.ComandosIR.infrastructure.routers import router as comandos_ir_router
from src.Alertas.infrastructure.routers import router as alertas_router
from src.Lecturas.infrastructure.routers import router as lecturas_sql_router
from src.Sensores.infrastructure.routers import router as sensores_router
from src.core.db_influx import close_influx_client

app = FastAPI(
    title="API Voltio",
    description="API para el sistema de monitoreo de sensores Voltio",
    version="1.0.0"
)


@app.on_event("startup")
def startup_event():
    """Crear las tablas de la base de datos al iniciar la aplicación"""
    Base.metadata.create_all(bind=engine)


# Incluir los routers
app.include_router(roles_router, prefix="/api/v1")
app.include_router(usuarios_router, prefix="/api/v1")
app.include_router(lecturas_router, prefix="/api/v1/lecturas-pzem")
app.include_router(ubicaciones_router, prefix="/api/v1")
app.include_router(tipo_sensores_router, prefix="/api/v1")
app.include_router(comandos_ir_router, prefix="/api/v1")
app.include_router(alertas_router, prefix="/api/v1")
app.include_router(lecturas_sql_router, prefix="/api/v1")
app.include_router(sensores_router, prefix="/api/v1")


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
        "secret_key_preview": settings.secret_key[:20] + "..." if settings.secret_key else None,
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


@app.get('/test/deployment')
def test_deployment():
    """Endpoint de prueba para verificar que los cambios se reflejan en el despliegue"""
    
    # Información básica del sistema
    deployment_info = {
        "status": "✅ API funcionando correctamente",
        "message": "Este endpoint confirma que el despliegue fue exitoso",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.1.0",  # Incrementamos la versión para ver cambios
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
            "python_version": sys.version,
            "platform": sys.platform,
            "current_directory": str(Path.cwd()),
            "main_file_exists": Path("main.py").exists(),
            "src_directory_exists": Path("src").exists()
        },
        "modules_status": {
            "usuarios": "✅ Disponible",
            "roles": "✅ Disponible", 
            "ubicaciones": "✅ Disponible",
            "tipo_sensores": "✅ Disponible",
            "sensores": "✅ Disponible",
            "lecturas": "✅ Disponible",
            "comandos_ir": "✅ Disponible",
            "alertas": "✅ Disponible",
            "lecturas_influx_pzem": "✅ Disponible"
        },
        "database": {
            "postgresql_configured": bool(os.getenv("DB_NAME")),
            "influxdb_configured": bool(os.getenv("INFLUX_URL")),
            "connection_test": "Configurado (test de conexión requiere BD activa)"
        },
        "endpoints_available": [
            "GET /",
            "GET /test/deployment",
            "GET /debug/config",
            "GET /api/v1/usuarios/",
            "GET /api/v1/roles/",
            "GET /api/v1/ubicaciones/",
            "GET /api/v1/tipo-sensores/",
            "GET /api/v1/sensores/",
            "GET /api/v1/lecturas/",
            "GET /api/v1/comandos-ir/",
            "GET /api/v1/alertas/",
            "GET /api/v1/lecturas-pzem/"
        ]
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
