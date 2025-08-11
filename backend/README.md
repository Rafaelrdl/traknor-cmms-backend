# TrakNor Backend

Este projeto configura uma base em Django com Django REST Framework, executada em contêineres Docker.

## Pré-requisitos
- Docker
- Docker Compose

## Configuração rápida
```bash
cp .env.example .env
docker compose build
docker compose up -d
```

As migrações são executadas automaticamente na inicialização. Para aplicar manualmente:
```bash
docker compose run --rm web python src/manage.py migrate
```

## Endpoints
- `GET /health` — verifica o estado da API.
- `GET /docs` — interface interativa da documentação.
- `GET /schema` — esquema OpenAPI em JSON.

## Comandos úteis
- Criar superusuário: `docker compose run --rm web python src/manage.py createsuperuser`
- Gerar migrações: `docker compose run --rm web python src/manage.py makemigrations`
```
