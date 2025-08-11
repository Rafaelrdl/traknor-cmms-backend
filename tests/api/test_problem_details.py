import pytest

from tenancy.models import Tenant, Domain


@pytest.fixture
def tenant() -> Tenant:
    """Cria um tenant para validar o tratamento de erros."""
    tenant = Tenant(schema_name="acme", name="ACME Ltd.")
    tenant.save()
    Domain.objects.create(domain="acme.localhost", tenant=tenant, is_primary=True)
    return tenant


@pytest.mark.django_db
def test_validation_error_returns_422(client, tenant):
    """POST inválido deve retornar Problem Details 422."""
    resp = client.post(
        "/_example",
        {},
        content_type="application/json",
        HTTP_HOST="acme.localhost",
    )
    assert resp.status_code == 422
    body = resp.json()
    assert body["status"] == 422
    assert body["title"] == "Validation Error"
    assert body["errors"][0]["name"] == "name"
    assert resp["Content-Type"] == "application/problem+json"


@pytest.mark.django_db
def test_not_found_returns_problem_details(client, tenant):
    """Recurso inexistente retorna 404 em Problem Details."""
    resp = client.get("/_example/999", HTTP_HOST="acme.localhost")
    assert resp.status_code == 404
    body = resp.json()
    assert body["status"] == 404
    assert body["title"] == "Not Found"


@pytest.mark.django_db
def test_internal_error_returns_problem_details(client, tenant):
    """Exceções não tratadas retornam 500 em Problem Details."""
    resp = client.get("/_error", HTTP_HOST="acme.localhost")
    assert resp.status_code == 500
    body = resp.json()
    assert body["status"] == 500
    assert body["title"] == "Internal Server Error"
