#!/bin/bash
set -e  # Detiene el script ante cualquier error

# Cargar variables del archivo .env (si existe)
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Validar variables necesarias para el superusuario
: "${DJANGO_SUPERUSER_USERNAME:=admin}"
: "${DJANGO_SUPERUSER_EMAIL:=admin@example.com}"
: "${DJANGO_SUPERUSER_PASSWORD:=admin123}"

echo "🧹 Limpiando contenedores antiguos..."
docker compose down -v || true

echo "🚀 Levantando contenedores Docker..."
docker compose up -d --build

# Esperar a que la base de datos esté lista
echo "⏳ Esperando a que la base de datos esté lista..."
until docker compose exec db pg_isready -U "$POSTGRES_USER" > /dev/null 2>&1; do
  echo -n "."
  sleep 2
done
echo "✅ Base de datos lista"

# Esperar a que el contenedor web esté corriendo
echo "⏳ Esperando a que el contenedor web esté activo..."
until docker compose ps | grep -q "web.*Up"; do
  echo -n "."
  sleep 2
done
echo "✅ Contenedor web activo"

# Instalar dependencias
echo "📦 Instalando dependencias..."
docker compose exec web pip install --upgrade pip
docker compose exec web pip install -r requirements.txt

# Migraciones
echo "📂 Ejecutando migraciones..."
docker compose exec web python manage.py migrate

# Archivos estáticos
echo "🗂 Recolectando archivos estáticos..."
docker compose exec web python manage.py collectstatic --noinput

# Crear superusuario automáticamente si no existe
echo "👤 Verificando superusuario..."
SUPERUSER_EXISTS=$(docker compose exec web python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
print(User.objects.filter(is_superuser=True).exists())
" | tr -d '\r')

if [ "$SUPERUSER_EXISTS" = "False" ]; then
  echo "⚡ Creando superusuario automáticamente..."
  docker compose exec web python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
username='$DJANGO_SUPERUSER_USERNAME';
email='$DJANGO_SUPERUSER_EMAIL';
password='$DJANGO_SUPERUSER_PASSWORD';
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
print('✅ Superusuario creado:', username)
"
else
  echo "👍 Superusuario ya existe."
fi

# Reiniciar Nginx (por si los estáticos cambiaron)
echo "🔄 Reiniciando Nginx..."
docker compose restart nginx

echo ""
echo "🎉 Todo listo! Admin disponible en: http://localhost:8000/admin/"
echo "👤 Usuario: $DJANGO_SUPERUSER_USERNAME"
echo "🔑 Contraseña: $DJANGO_SUPERUSER_PASSWORD"
echo ""
