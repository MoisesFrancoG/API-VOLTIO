from fastapi import FastAPI
from src.core.db import engine, Base
from src.Roles.infrastructure.routers import router as roles_router
from src.Lecturas_influx_pzem.infrastructure.routers import router as lecturas_router
from src.core.db_influx import close_influx_client

# Crear las tablas de la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Voltio",
    description="API para el sistema de monitoreo de sensores Voltio",
    version="1.0.0"
)

# Incluir los routers
app.include_router(roles_router, prefix="/api/v1")
app.include_router(lecturas_router, prefix="/api/v1/lecturas-pzem")


@app.on_event("shutdown")
def shutdown_event():
    close_influx_client()

@app.get('/')
def read_root():
    return {'message': 'Api de voltio iniciada'}

