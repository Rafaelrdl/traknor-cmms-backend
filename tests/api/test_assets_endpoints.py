"""Testes básicos dos endpoints de ativos e estrutura."""

import pytest
from django_tenants.utils import schema_context
from django.contrib.auth import get_user_model

from tenancy.models import Tenant, Domain
from django_tenants.utils import get_public_schema_name
from accounts.models import Membership
from accounts.roles import Role
from assets.models import Asset, Company, Sector, Subsection
from rest_framework.authtoken.models import Token


@pytest.fixture
def tenant(db):
    """Cria um tenant simples para os testes."""
    tenant = Tenant(schema_name="acme", name="ACME Ltd.")
    with schema_context(get_public_schema_name()):
        tenant.save()
        Domain.objects.create(domain="acme.localhost", tenant=tenant, is_primary=True)
    return tenant


@pytest.fixture
def admin_user(tenant):
    """Usuário com papel de administrador e token para autenticação."""
    User = get_user_model()
    with schema_context(tenant.schema_name):
        user = User.objects.create_user("admin", "admin@example.com", "senha123")
        Membership.objects.create(user=user, tenant=tenant, role=Role.ADMIN.value)
        token, _ = Token.objects.get_or_create(user=user)
    return user, token.key


@pytest.fixture
def sample_data(tenant):
    """Estrutura básica com um ativo cadastrado."""
    with schema_context(tenant.schema_name):
        company = Company.objects.create(name="Hosp", status="active")
        sector = Sector.objects.create(company=company, name="UTI", status="active")
        subsection = Subsection.objects.create(
            sector=sector, name="Sala 1", status="active"
        )
        asset = Asset.objects.create(
            code="A1",
            type="ahu",
            status="active",
            brand="X",
            model="Y",
            company=company,
            sector=sector,
            subsection=subsection,
        )
    return {
        "company": company,
        "sector": sector,
        "subsection": subsection,
        "asset": asset,
    }


@pytest.mark.django_db
def test_locations_tree_returns_counts(client, tenant, admin_user, sample_data):
    """A árvore deve incluir contagens corretas de equipamentos."""
    user, token = admin_user
    resp = client.get(
        "/locations/tree",
        HTTP_HOST="acme.localhost",
        HTTP_AUTHORIZATION=f"Token {token}",
    )
    assert resp.status_code == 200
    tree = resp.json()["data"]
    assert tree[0]["equipment_count"] == 1
    assert tree[0]["sectors"][0]["subsections"][0]["equipment_count"] == 1


@pytest.mark.django_db
def test_equipment_alias_matches_assets(client, tenant, admin_user, sample_data):
    """/equipment deve ser espelho de /assets."""
    user, token = admin_user
    headers = {"HTTP_HOST": "acme.localhost", "HTTP_AUTHORIZATION": f"Token {token}"}
    resp_assets = client.get("/assets/", **headers)
    resp_equipment = client.get("/equipment/", **headers)
    assert resp_assets.json()["data"] == resp_equipment.json()["data"]


@pytest.mark.django_db
def test_asset_utilization_endpoint(client, tenant, admin_user, sample_data):
    """Endpoint de utilização deve retornar estrutura padrão."""
    user, token = admin_user
    asset_id = sample_data["asset"].id
    url = f"/assets/{asset_id}/utilization/?range=7d&granularity=day"
    resp = client.get(
        url,
        HTTP_HOST="acme.localhost",
        HTTP_AUTHORIZATION=f"Token {token}",
    )
    assert resp.status_code == 200
    body = resp.json()["data"]
    assert "series" in body and "indicators" in body

