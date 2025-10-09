#!/bin/bash
set -e

echo "🧹 Limpiando contenedores antiguos..."
docker compose down -v || true

echo "🚀 Levantando contenedores Docker..."
docker compose up -d --build

# Espera a la DB
echo "⏳ Esperando a que la DB esté lista..."
until docker compose exec db pg_isready -U sisadmi > /dev/null 2>&1; do
    echo -n "."
    sleep 2
done
echo "✅ DB lista"

# Espera a que el contenedor web esté activo
echo "⏳ Esperando a que el contenedor web esté activo..."
until docker compose exec db echo "web listo" > /dev/null 2>&1; do
    echo -n "."
    sleep 2
done
echo "✅ Web lista"

# Instala dependencias
echo "📦 Instalando dependencias..."
docker compose exec db pip install --upgrade pip
docker compose exec db pip install -r requirements.txt

# Migraciones
echo "📂 Ejecutando migraciones..."
docker compose exec db python manage.py migrate

# Collect static
echo "🗂 Recolectando archivos estáticos..."
docker compose exec db python manage.py collectstatic --noinput

# Superusuario
echo "👤 Verificando superusuario..."
SUPERUSER_EXISTS=$(docker compose exec db python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(is_superuser=True).exists())" | tr -d '\r')
if [ "$SUPERUSER_EXISTS" = "False" ]; then
    echo "⚡ Creando superusuario..."
    docker compose exec -it db python manage.py createsuperuser
else
    echo "👍 Superusuario ya existe."
fi

# Reiniciar Nginx
echo "🔄 Reiniciando Nginx..."
docker compose restart nginx

echo "🎉 Todo listo! Admin disponible en http://localhost:8080/admin/"
