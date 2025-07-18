from fastapi import FastAPI
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


@app.get('/debug/token')
def get_debug_token(user_email: str = "admin@voltio.com"):
    """Endpoint para obtener un token JWT para pruebas (solo en desarrollo)"""
    if settings.environment != "development":
        return {"error": "Este endpoint solo está disponible en modo desarrollo"}

    try:
        # Importar las dependencias necesarias
        from src.Usuarios.infrastructure.database import get_usuario_use_cases
        from src.core.db import get_database
        from sqlalchemy.orm import Session

        # Obtener una sesión de base de datos
        db_gen = get_database()
        db = next(db_gen)

        try:
            # Obtener el caso de uso de usuarios
            usuario_use_cases = get_usuario_use_cases(db)

            # Buscar el usuario por email
            from sqlalchemy import text
            with db.bind.connect() as conn:
                result = conn.execute(text("""
                    SELECT id_usuario, nombre_usuario, correo, id_rol 
                    FROM usuarios 
                    WHERE correo = :email
                """), {"email": user_email})
                
                user_data = result.fetchone()
                
                if not user_data:
                    return {
                        "error": f"Usuario con email '{user_email}' no encontrado",
                        "available_users": "Usa /debug/users para ver usuarios disponibles"
                    }

                # Crear el token JWT manualmente
                from datetime import datetime, timedelta
                from jose import jwt
                
                # Datos del payload
                payload_data = {
                    "sub": str(user_data[0]),  # id_usuario
                    "email": user_data[2],     # correo
                    "exp": datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
                }
                
                # Generar el token
                access_token = jwt.encode(
                    payload_data, 
                    settings.secret_key, 
                    algorithm="HS256"
                )

                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "expires_in": settings.access_token_expire_minutes * 60,
                    "user_info": {
                        "id": user_data[0],
                        "nombre": user_data[1],
                        "email": user_data[2],
                        "rol_id": user_data[3]
                    },
                    "usage": f"Authorization: Bearer {access_token}",
                    "note": "Este token es solo para desarrollo y pruebas"
                }

        finally:
            db.close()

    except Exception as e:
        return {
            "error": f"Error al generar token: {str(e)}",
            "suggestion": "Asegúrate de que la base de datos esté disponible y el usuario exista"
        }


@app.get('/debug/users')
def get_debug_users():
    """Endpoint para listar usuarios disponibles para debug (solo en desarrollo)"""
    if settings.environment != "development":
        return {"error": "Este endpoint solo está disponible en modo desarrollo"}

    try:
        from src.core.db import get_database
        from sqlalchemy import text

        # Obtener una sesión de base de datos
        db_gen = get_database()
        db = next(db_gen)

        try:
            with db.bind.connect() as conn:
                result = conn.execute(text("""
                    SELECT u.id_usuario, u.nombre_usuario, u.correo, r.nombre as rol_nombre
                    FROM usuarios u
                    LEFT JOIN roles r ON u.id_rol = r.id_rol
                    ORDER BY u.id_usuario
                """))
                
                users = []
                for row in result:
                    users.append({
                        "id": row[0],
                        "nombre": row[1], 
                        "email": row[2],
                        "rol": row[3]
                    })

                return {
                    "users": users,
                    "total": len(users),
                    "usage": "Usa /debug/token?user_email=EMAIL para obtener token de cualquier usuario"
                }

        finally:
            db.close()

    except Exception as e:
        return {
            "error": f"Error al obtener usuarios: {str(e)}"
        }
