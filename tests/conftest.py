"""Configurações globais para testes."""

import pytest
from django.conf import settings
from django_tenants.utils import schema_context
from tenancy.models import Tenant, Domain


@pytest.fixture
def tenant(db):
    """Cria tenant básico para os testes."""
    # Força criação do tenant no schema público
    with schema_context('public'):
        tenant = Tenant(schema_name="acme", name="ACME")
        tenant.save()
        Domain.objects.create(domain="acme.localhost", tenant=tenant, is_primary=True)
    return tenant


@pytest.fixture  
def tenant_client(client, tenant):
    """Cliente HTTP configurado com o host correto para multi-tenancy."""
    client.defaults["HTTP_HOST"] = "acme.localhost"
    return client
