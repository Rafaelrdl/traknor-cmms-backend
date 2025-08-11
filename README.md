# TrakNor CMMS Backend

## Multitenancy

### Preparação
1. Copie o arquivo de exemplo: `cp .env.example .env`.
2. Ajuste o `/etc/hosts` local adicionando:
   ```
   127.0.0.1 acme.localhost beta.localhost
   ```

### Subindo o ambiente
```bash
docker compose up --build
```

### Migrações por schema
```bash
python manage.py migrate_schemas --shared
python manage.py migrate_schemas --tenant
python manage.py seed_tenants
```

### Testando
- `http://localhost:8000/health` → schema `public`
- `http://acme.localhost:8000/health` → schema `acme`
- `http://beta.localhost:8000/health` → schema `beta`

### Criando novo tenant
```bash
python manage.py create_tenant --schema=novo --name="Novo" --domain=novo.localhost --primary
```
