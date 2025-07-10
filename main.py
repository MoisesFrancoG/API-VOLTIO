from fastapi import FastAPI
from src.core.db import engine, Base
from src.Roles.infrastructure.routers import router as roles_router

# Crear las tablas de la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Voltio",
    description="API para el sistema de monitoreo de sensores Voltio",
    version="1.0.0"
)

# Incluir los routers
app.include_router(roles_router, prefix="/api/v1")


@app.get('/')
def read_root():
    return {'message': 'Api de voltio iniciada'}
