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
    DB_USER = os.getenv("DB_USER", "usuario")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "contraseña")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    
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
