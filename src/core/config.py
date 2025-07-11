"""
Configuración de la aplicación
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configuración de la aplicación"""
    
    # Database
    DB_NAME = os.getenv("DB_NAME", "voltio")
    DB_USER = os.getenv("DB_USER", "voltio_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "voltio_pass")
    DB_HOST = os.getenv("DB_HOST", "18.214.35.249")
    DB_PORT = os.getenv("DB_PORT", "5432")
    # InfluxDB
    INFLUX_URL = os.getenv("INFLUX_URL", "http://52.201.107.193:8086")
    INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "lJLzxtHLHvPNgdvU9dcInGYb/qLbLxUPgrePzLd47EKCLUWBzJ+RmJkpH0f1HkmQ")
    INFLUX_ORG = os.getenv("INFLUX_ORG", "mi-org")
    INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "sensores")
    
    # Database URL
    database_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # API
    api_title = "API Voltio"
    api_description = "API para el sistema de monitoreo de sensores Voltio"
    api_version = "1.0.0"
    
    # Security
    secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")
    access_token_expire_minutes = 30
    
    # Environment
    environment = os.getenv("ENVIRONMENT", "development")
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    


settings = Settings()
