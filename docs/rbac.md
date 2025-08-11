# RBAC inicial

Este documento descreve a implementação inicial de controle de acesso baseado em papéis.

## Papéis

- **admin**: acesso total ao tenant.
- **technician**: acesso de leitura e atualização apenas quando responsável.
- **requester**: pode criar e visualizar seus próprios registros.

## Uso nas views

```python
from core.mixins import RoleRequiredMixin, TenantScopedMixin, OwnershipQuerysetMixin
from core.permissions import IsOwnerOrAdmin

class MinhaViewSet(RoleRequiredMixin, TenantScopedMixin, OwnershipQuerysetMixin, ModelViewSet):
    required_roles_read = ("admin", "technician", "requester")
    required_roles_write = ("admin",)
    object_level_permissions = [IsOwnerOrAdmin]
    ownership_field = "created_by"
```

## Ownership

- `IsOwnerOrAdmin`: compara `created_by`.
- `IsAssigneeOrAdmin`: compara `assignee`.
- `IsRequesterSelfOrAdmin`: compara `requester`.

## Seed

Use `python manage.py seed_rbac` para criar um tenant demo com usuários de cada papel.
