# ==============================================================================
# DOCKERFILE PARA API VOLTIO - FASTAPI CON POSTGRESQL E INFLUXDB
# Multi-stage build para optimizar tamaño de imagen
# ==============================================================================

# ------------------------------------------------------------------------------
# STAGE 1: Builder - Instala dependencias
# ------------------------------------------------------------------------------
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Crear un virtual environment e instalar dependencias
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ------------------------------------------------------------------------------
# STAGE 2: Runtime - Imagen final optimizada
# ------------------------------------------------------------------------------
FROM python:3.11-slim

WORKDIR /app

# Crear usuario no-root para ejecutar la aplicación (seguridad)
RUN useradd -m -u 1000 voltio && \
    chown -R voltio:voltio /app

# Instalar solo librerías runtime necesarias (no compiladores)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar el virtual environment desde el builder
COPY --from=builder /opt/venv /opt/venv

# Configurar PATH para usar el venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar código fuente de la aplicación
COPY --chown=voltio:voltio . .

# Variables de entorno por defecto (pueden sobrescribirse)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    HOST=0.0.0.0 \
    WORKERS=4

# Exponer puerto de la aplicación
EXPOSE 8000

# Cambiar a usuario no-root
USER voltio

# Health check para verificar que la API responde
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Comando para iniciar la aplicación con Uvicorn
# Usa variables de entorno para configuración flexible
CMD uvicorn main:app \
    --host ${HOST} \
    --port ${PORT} \
    --workers ${WORKERS} \
    --log-level info \
    --proxy-headers \
    --forwarded-allow-ips "*"
