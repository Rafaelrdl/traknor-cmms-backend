from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Tenant(TenantMixin):
    """Modelo que representa um tenant, cada um com seu próprio schema."""
    name = models.CharField(max_length=200)
    plan = models.CharField(max_length=50, default="mvp")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auto_create_schema = True  # cria automaticamente o schema ao salvar

    def __str__(self) -> str:  # pragma: no cover - método simples
        # retorna nome do schema e nome amigável
        return f"{self.schema_name} ({self.name})"


class Domain(DomainMixin):
    """Relaciona domínios/subdomínios a um tenant."""
    is_primary = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.domain
