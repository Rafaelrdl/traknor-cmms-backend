FROM python:3.12-slim

# Instala dependências de compilação mínimas
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cria usuário não root para executar a aplicação
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 8000

CMD ["/app/entrypoint.sh"]
