"""
Configuración de la aplicación
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


class Settings:
    """Configuración de la aplicación"""
    
    # Base de datos PostgreSQL
    db_name: str = os.getenv("DB_NAME")
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")
    
    # Construir la URL de la base de datos
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    # InfluxDB
    influx_url: str = os.getenv("INFLUX_URL")
    influx_token: str = os.getenv("INFLUX_TOKEN")
    influx_org: str = os.getenv("INFLUX_ORG")
    influx_bucket: str = os.getenv("INFLUX_BUCKET")
    
    # JWT
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Configuración de la app
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"


# Instancia global de configuración
settings = Settings()
