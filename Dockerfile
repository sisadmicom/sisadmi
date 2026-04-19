# Imagen base
FROM python:3.12-slim

# Directorio de trabajo
WORKDIR /app
#WORKDIR /app/src

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    postgresql-client \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY ./src /app

# Copiar script de espera y dar permisos
COPY ./src/wait_for_db.sh /app/wait_for_db.sh
RUN chmod +x /app/wait_for_db.sh

# Crear carpeta para archivos estáticos
RUN mkdir -p /app/staticfiles

# Comando por defecto
CMD ["bash", "-c", "/app/wait_for_db.sh && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
