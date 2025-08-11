FROM python:3.11-slim

# diretório de trabalho
WORKDIR /app

# instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copia o projeto
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
