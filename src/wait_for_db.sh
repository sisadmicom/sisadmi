#!/bin/bash
set -euo pipefail

# Valores por defecto si no están definidos
host="${POSTGRES_HOST:-db}"
port="${POSTGRES_PORT:-5432}"
user="${POSTGRES_USER:-sisadmi}"
db="${POSTGRES_DB:-sisadmi-db}"
#b="${POSTGRES_DB:-sisadmi}"
# Espera hasta que postgres responda
until PGPASSWORD="${POSTGRES_PASSWORD:-}" psql -h "$host" -p "$port" -U "$user" -d "$db" -c '\q' >/dev/null 2>&1; do
  >&2 echo "❌ PostgreSQL no está disponible todavía en ${host}:${port}, reintentando en 5s..."
  sleep 5
done

>&2 echo "✅ PostgreSQL está disponible, continuando..."

# Aplicar migraciones (silenciosas)
echo "🔄 Aplicando migraciones de Django..."
python manage.py migrate --noinput

# Ejecutar el comando que se pase al container (por ejemplo runserver o gunicorn)
exec "$@"
