#!/bin/bash
set -e  # Detener script si ocurre un error

# Función para esperar a que la base de datos esté lista
wait_for_db() {
    echo "⏳ Esperando a que la base de datos esté lista..."
    until docker compose exec db pg_isready -U sisadmi > /dev/null 2>&1; do
        echo -n "."
        sleep 2
    done
    echo "✅ Base de datos lista."
}

echo "🚀 Levantando contenedores Docker..."
docker compose up -d --build

wait_for_db

echo "📦 Ejecutando migraciones..."
docker compose exec web python manage.py migrate

echo "🗂 Recolectando archivos estáticos..."
docker compose exec web python manage.py collectstatic --noinput

# Crear superusuario si no existe
echo "👤 Verificando si existe superusuario..."
SUPERUSER_EXISTS=$(docker compose exec web python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(is_superuser=True).exists())" | tr -d '\r')
if [ "$SUPERUSER_EXISTS" = "False" ]; then
    echo "⚡ Creando superusuario (interactivo)..."
    docker compose exec -it web python manage.py createsuperuser
else
    echo "👍 Superusuario ya existe."
fi

# Reiniciar Nginx para cargar archivos estáticos
echo "🔄 Reiniciando Nginx..."
docker compose restart nginx

echo "✅ Todo listo. Admin disponible en http://localhost:8080/admin/"
