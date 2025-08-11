import pytest
from django_tenants.utils import schema_context
from django.contrib.auth import get_user_model

from tenancy.models import Tenant, Domain
from accounts.models import Membership
from accounts.roles import Role


@pytest.fixture
def tenant(db):
    """Cria um tenant simples para os testes."""
    tenant = Tenant(schema_name="acme", name="ACME Ltd.")
    tenant.save()
    Domain.objects.create(domain="acme.localhost", tenant=tenant, is_primary=True)
    return tenant


@pytest.fixture
def user(tenant):
    """Cria um usuário associado ao tenant."""
    User = get_user_model()
    with schema_context(tenant.schema_name):
        user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="senha123",
            first_name="John",
            last_name="Doe",
        )
        Membership.objects.create(
            user=user, tenant=tenant, role=Role.TECHNICIAN.value
        )
    return user


@pytest.mark.django_db
def test_me_endpoint_returns_user_data(client, tenant, user):
    """Verifica se o endpoint retorna os dados do usuário autenticado."""
    client.force_login(user)
    resp = client.get("/users/me", HTTP_HOST="acme.localhost")
    assert resp.status_code == 200
    body = resp.json()["data"]
    assert body["email"] == "john@example.com"
    assert body["role"] == Role.TECHNICIAN.value


@pytest.mark.django_db
def test_me_endpoint_requires_authentication(client, tenant):
    """Requisições sem autenticação devem retornar 401."""
    resp = client.get("/users/me", HTTP_HOST="acme.localhost")
    assert resp.status_code == 401
