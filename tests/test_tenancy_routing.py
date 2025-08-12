import pytest
from django_tenants.utils import schema_context
from tenancy.models import Tenant, Domain


@pytest.mark.django_db
def test_routing_by_host(client):
    """Verifica se cada host aponta para o schema correto."""
    with schema_context('public'):
        acme = Tenant(schema_name="acme", name="ACME Ltd.")
        acme.save()
        Domain.objects.create(domain="acme.localhost", tenant=acme, is_primary=True)

        beta = Tenant(schema_name="beta", name="Beta Ltd.")
        beta.save()
        Domain.objects.create(domain="beta.localhost", tenant=beta, is_primary=True)

    resp_acme = client.get("/health", HTTP_HOST="acme.localhost")
    assert resp_acme.status_code == 200
    assert resp_acme.json()["schema"] == "acme"

    resp_beta = client.get("/health", HTTP_HOST="beta.localhost")
    assert resp_beta.status_code == 200
    assert resp_beta.json()["schema"] == "beta"
