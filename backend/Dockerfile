FROM python:3.12-slim

# Instala dependências de compilação mínimas e cliente PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Define o diretório de trabalho como src onde está o manage.py
WORKDIR /app/src

# Torna o entrypoint.sh executável
RUN chmod +x /app/entrypoint.sh

# Cria usuário não root para executar a aplicação
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 8000

CMD ["/app/entrypoint.sh"]
