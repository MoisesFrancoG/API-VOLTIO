"""
Configuración de la aplicación
"""
import pathlib
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
env_path = pathlib.Path(__file__).parent.parent.parent / ".env"

# override=True asegura que las variables del .env sobrescriban las del sistema
load_dotenv(dotenv_path=env_path, override=True)


class Settings:
    """Configuración de la aplicación"""

    def __init__(self):
        # Validar que las variables requeridas estén presentes
        required_vars = [
            "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT",
            "INFLUX_URL", "INFLUX_TOKEN", "INFLUX_ORG", "INFLUX_BUCKET",
            "SECRET_KEY"
        ]

        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(
                f"Variables de entorno requeridas faltantes: {missing_vars}")

        # Inicializar túnel SSH si está habilitado
        self._init_ssh_tunnel()

    def _init_ssh_tunnel(self):
        """Inicializar túnel SSH automáticamente si está configurado"""
        tunnel_enabled = os.getenv(
            "SSH_TUNNEL_ENABLED", "false").lower() == "true"

        if tunnel_enabled:
            try:
                from .ssh_tunnel import create_tunnel_from_env
                tunnel = create_tunnel_from_env()
                if tunnel:
                    # Verificar si el túnel ya está activo
                    active, pid = tunnel.status()
                    if not active:
                        print("🔄 Iniciando túnel SSH automáticamente...")
                        if tunnel.start_tunnel():
                            print("✅ Túnel SSH establecido automáticamente")
                        else:
                            print("⚠️ No se pudo establecer el túnel SSH automático")
                    else:
                        print(f"✅ Túnel SSH ya activo (PID: {pid})")
            except ImportError:
                print(
                    "⚠️ Módulo ssh_tunnel no disponible. Instalar psutil: pip install psutil")
            except Exception as e:
                print(f"⚠️ Error configurando túnel SSH automático: {e}")

    # Base de datos PostgreSQL
    @property
    def db_name(self) -> str:
        return os.getenv("DB_NAME")

    @property
    def db_user(self) -> str:
        return os.getenv("DB_USER")

    @property
    def db_password(self) -> str:
        return os.getenv("DB_PASSWORD")

    @property
    def db_host(self) -> str:
        return os.getenv("DB_HOST")

    @property
    def db_port(self) -> str:
        return os.getenv("DB_PORT")

    # Construir la URL de la base de datos
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    # InfluxDB
    @property
    def influx_url(self) -> str:
        return os.getenv("INFLUX_URL")

    @property
    def influx_token(self) -> str:
        return os.getenv("INFLUX_TOKEN")

    @property
    def influx_org(self) -> str:
        return os.getenv("INFLUX_ORG")

    @property
    def influx_bucket(self) -> str:
        return os.getenv("INFLUX_BUCKET")

    # JWT
    @property
    def secret_key(self) -> str:
        return os.getenv("SECRET_KEY")

    @property
    def algorithm(self) -> str:
        return "HS256"

    @property
    def access_token_expire_minutes(self) -> int:
        return int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Configuración de la app
    @property
    def environment(self) -> str:
        return os.getenv("ENVIRONMENT", "development")

    @property
    def debug(self) -> bool:
        return os.getenv("DEBUG", "true").lower() == "true"

    # Configuración del túnel SSH
    @property
    def ssh_tunnel_enabled(self) -> bool:
        return os.getenv("SSH_TUNNEL_ENABLED", "false").lower() == "true"

    @property
    def ssh_tunnel_info(self) -> dict:
        """Información del túnel SSH"""
        return {
            "enabled": self.ssh_tunnel_enabled,
            "remote_host": os.getenv("SSH_TUNNEL_REMOTE_HOST"),
            "ssh_user": os.getenv("REMOTE_SSH_USER"),
            "local_port": os.getenv("SSH_TUNNEL_LOCAL_PORT", "5432"),
            "remote_port": os.getenv("SSH_TUNNEL_REMOTE_PORT", "5432"),
            "ssh_key_path": os.getenv("SSH_KEY_PATH")
        }

    # Configuración SMTP para emails
    @property
    def smtp_server(self) -> str:
        return os.getenv("SMTP_SERVER", "smtp.gmail.com")

    @property
    def smtp_port(self) -> int:
        return int(os.getenv("SMTP_PORT", "587"))

    @property
    def smtp_username(self) -> str:
        return os.getenv("SMTP_USERNAME", "")

    @property
    def smtp_password(self) -> str:
        return os.getenv("SMTP_PASSWORD", "")

    @property
    def from_email(self) -> str:
        return os.getenv("FROM_EMAIL", os.getenv("SMTP_USERNAME", ""))

    @property
    def notification_email_enabled(self) -> bool:
        """Verifica si el servicio de email está habilitado"""
        return bool(self.smtp_username and self.smtp_password)

    # ============================================
    # 🌐 CONFIGURACIÓN CORS
    # ============================================
    
    @property
    def cors_origins(self) -> list[str]:
        """Obtener orígenes permitidos para CORS según el ambiente"""
        
        # Orígenes desde variable de entorno (separados por coma)
        env_origins = os.getenv("CORS_ORIGINS", "")
        if env_origins:
            return [origin.strip() for origin in env_origins.split(",")]
        
        # Configuración por defecto según ambiente
        if self.environment == "development":
            return [
                "http://localhost:3000",        # React default
                "http://localhost:3001",        # React alternate
                "http://localhost:8080",        # Vue.js default
                "http://localhost:8081",        # Vue.js alternate
                "http://localhost:4200",        # Angular default
                "http://localhost:5000",        # Flask/Python
                "http://localhost:5173",        # Vite default
                "http://127.0.0.1:3000",        # localhost alternative
                "http://127.0.0.1:8080",
                "http://127.0.0.1:5173",
                "http://0.0.0.0:3000",          # Docker containers
                "http://0.0.0.0:8080",
            ]
        else:
            # Producción: Solo dominios específicos
            return [
                "https://voltio-dashboard.acstree.xyz",
                "https://voltio-admin.acstree.xyz", 
                "https://voltio-mobile.acstree.xyz",
                "https://dashboard.voltio.com",
                "https://admin.voltio.com",
                "https://app.voltio.com",
            ]
    
    @property
    def cors_allow_credentials(self) -> bool:
        """Permitir credenciales en CORS"""
        return os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    
    @property
    def cors_allow_methods(self) -> list[str]:
        """Métodos HTTP permitidos en CORS"""
        methods = os.getenv("CORS_ALLOW_METHODS", "GET,POST,PUT,PATCH,DELETE,OPTIONS")
        return [method.strip() for method in methods.split(",")]
    
    @property
    def cors_allow_headers(self) -> list[str]:
        """Headers permitidos en CORS"""
        headers = os.getenv("CORS_ALLOW_HEADERS", 
            "Authorization,Content-Type,Accept,Origin,X-Requested-With,Access-Control-Request-Method,Access-Control-Request-Headers")
        return [header.strip() for header in headers.split(",")]
    
    @property
    def cors_expose_headers(self) -> list[str]:
        """Headers expuestos en CORS"""
        headers = os.getenv("CORS_EXPOSE_HEADERS", "X-Total-Count,X-Rate-Limit,X-API-Version")
        return [header.strip() for header in headers.split(",")]
    
    @property
    def cors_max_age(self) -> int:
        """Tiempo de cache para preflight requests (segundos)"""
        return int(os.getenv("CORS_MAX_AGE", "600"))  # 10 minutos por defecto


# Instancia global de configuración
settings = Settings()
