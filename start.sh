#!/bin/bash
set -e  # Detener script si ocurre un error

echo "🚀 Levantando contenedores Docker..."
docker compose up -d --build

echo "⏳ Esperando a que la base de datos esté lista..."
sleep 10  # Ajusta si tu DB tarda más en inicializar

echo "📦 Ejecutando migraciones..."
docker compose exec web python manage.py migrate

echo "🗂 Recolectando archivos estáticos..."
docker compose exec web python manage.py collectstatic --noinput

echo "👤 Creando superusuario (opcional, interactivo)..."
docker compose exec -it web python manage.py createsuperuser || echo "Superusuario ya existe o cancelado."

echo "✅ Todo listo. Admin disponible en http://localhost:8080/admin/"
