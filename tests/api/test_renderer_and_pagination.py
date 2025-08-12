import pytest
from django_tenants.utils import schema_context

from tenancy.models import Tenant, Domain
from sample.models import SampleModel


@pytest.fixture
def tenant(db) -> Tenant:
    """Cria um tenant simples para os testes."""
    with schema_context('public'):
        tenant = Tenant(schema_name="acme", name="ACME Ltd.")
        tenant.save()
        Domain.objects.create(domain="acme.localhost", tenant=tenant, is_primary=True)
    return tenant


@pytest.mark.django_db
def test_list_with_pagination(client, tenant):
    """Verifica listagem paginada com envelope e headers."""
    with schema_context(tenant.schema_name):
        for i in range(60):
            SampleModel.objects.create(name=f"item-{i}")

    resp = client.get(
        "/_example", {"page": 2, "per_page": 25}, HTTP_HOST="acme.localhost"
    )
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["data"]) == 25
    assert body["meta"] == {
        "page": 2,
        "per_page": 25,
        "total_pages": 3,
        "total_items": 60,
    }
    assert set(body["links"]) == {"self", "first", "prev", "next", "last"}

    assert resp["X-Total-Count"] == "60"
    assert resp["X-Total-Pages"] == "3"
    assert resp["X-Per-Page"] == "25"
    assert resp["X-Current-Page"] == "2"
    for rel in ["first", "prev", "next", "last"]:
        assert f'rel="{rel}"' in resp["Link"]


@pytest.mark.django_db
def test_per_page_above_max_is_capped(client, tenant):
    """per_page acima de 100 é limitado e refletido no meta."""
    with schema_context(tenant.schema_name):
        for i in range(150):
            SampleModel.objects.create(name=f"item-{i}")

    resp = client.get(
        "/_example", {"per_page": 1000}, HTTP_HOST="acme.localhost"
    )
    body = resp.json()
    assert body["meta"]["per_page"] == 100
    assert resp["X-Per-Page"] == "100"


@pytest.mark.django_db
def test_page_out_of_range_returns_404(client, tenant):
    """Página inexistente resulta em Problem Details 404."""
    with schema_context(tenant.schema_name):
        SampleModel.objects.create(name="only-one")

    resp = client.get(
        "/_example", {"page": 999}, HTTP_HOST="acme.localhost"
    )
    assert resp.status_code == 404
    body = resp.json()
    assert body["status"] == 404
    assert body["title"] == "Not Found"
    assert resp["Content-Type"] == "application/problem+json"


@pytest.mark.django_db
def test_detail_and_create_envelope(client, tenant):
    """Detalhe e criação devem usar o envelope básico."""
    with schema_context(tenant.schema_name):
        obj = SampleModel.objects.create(name="item-1")

    detail = client.get(f"/_example/{obj.id}", HTTP_HOST="acme.localhost")
    assert detail.status_code == 200
    assert detail.json() == {"data": {"id": obj.id, "name": "item-1"}}

    create = client.post(
        "/_example",
        {"name": "novo"},
        content_type="application/json",
        HTTP_HOST="acme.localhost",
    )
    assert create.status_code == 201
    assert create.json()["data"]["name"] == "novo"
