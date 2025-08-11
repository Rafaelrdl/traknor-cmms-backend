#!/bin/sh
# Aguarda o banco de dados ficar disponível antes de iniciar a aplicação.
set -e

until pg_isready -d "$DATABASE_URL"; do
  echo "Aguardando o banco de dados..."
  sleep 1
done

# Executa migrações pendentes.
python src/manage.py migrate --noinput

# Inicia o servidor WSGI usando gunicorn.
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
