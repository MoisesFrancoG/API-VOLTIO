"""
Script para crear la tabla de sensores en la base de datos
"""

from sqlalchemy import create_engine, text
from src.core.config import settings

def crear_tabla_sensores():
    """Crear tabla de sensores si no existe"""
    
    # Crear conexión con la base de datos
    engine = create_engine(settings.DATABASE_URL)
    
    # SQL para crear la tabla
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS sensores (
        id_sensor INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(100) NOT NULL UNIQUE,
        id_tipo_sensor INTEGER NOT NULL,
        id_ubicacion INTEGER NOT NULL,
        id_usuario INTEGER NOT NULL,
        activo BOOLEAN DEFAULT 1 NOT NULL
    );
    """
    
    # SQL para crear índices
    sql_create_indexes = [
        "CREATE INDEX IF NOT EXISTS idx_sensores_nombre ON sensores(nombre);",
        "CREATE INDEX IF NOT EXISTS idx_sensores_tipo ON sensores(id_tipo_sensor);",
        "CREATE INDEX IF NOT EXISTS idx_sensores_ubicacion ON sensores(id_ubicacion);",
        "CREATE INDEX IF NOT EXISTS idx_sensores_usuario ON sensores(id_usuario);",
        "CREATE INDEX IF NOT EXISTS idx_sensores_activo ON sensores(activo);"
    ]
    
    try:
        with engine.connect() as conn:
            # Crear tabla
            conn.execute(text(sql_create_table))
            print("✓ Tabla 'sensores' creada exitosamente")
            
            # Crear índices
            for idx_sql in sql_create_indexes:
                conn.execute(text(idx_sql))
                print("✓ Índice creado exitosamente")
            
            conn.commit()
            print("✓ Migración completada exitosamente")
            
    except Exception as e:
        print(f"✗ Error al crear la tabla: {e}")
        raise

if __name__ == "__main__":
    crear_tabla_sensores()
