"""Testes para CORS e rate limiting."""

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from tenancy.models import Domain, Tenant


def _preflight(client: APIClient, path: str, origin: str):
    """Executa uma requisição OPTIONS simulando preflight."""
    return client.options(
        path,
        HTTP_ORIGIN=origin,
        HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        HTTP_ACCESS_CONTROL_REQUEST_HEADERS="Authorization, Content-Type",
        secure=True,
    )


@pytest.mark.django_db
def test_cors_preflight_allowed(client):
    """Origem permitida deve receber todos os headers de CORS."""
    resp = _preflight(client, "/health", "http://localhost:5173")
    assert resp.status_code in {200, 204}
    assert resp["Access-Control-Allow-Origin"] == "http://localhost:5173"
    assert "GET" in resp["Access-Control-Allow-Methods"]
    assert "Authorization" in resp["Access-Control-Allow-Headers"]
    assert resp["Access-Control-Allow-Credentials"] == "true"
    assert resp["Access-Control-Max-Age"] == "600"


@pytest.mark.django_db
def test_cors_preflight_blocked(client):
    """Origem não listada não deve receber headers CORS."""
    resp = _preflight(client, "/health", "http://malicioso.com")
    assert resp.status_code in {200, 204}
    assert "Access-Control-Allow-Origin" not in resp.headers


@pytest.mark.django_db
def test_login_throttling(client, settings):
    """Excesso de tentativas de login deve retornar 429."""
    # Reduz o limite para acelerar o teste
    rates = settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"].copy()
    rates["auth_login"] = "2/min"
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = rates

    url = reverse("auth-login")
    for _ in range(2):
        client.post(url)

    resp = client.post(url)
    assert resp.status_code == 429
    body = resp.json()
    assert body["status"] == 429
    assert body["title"] == "Too Many Requests"


@pytest.fixture
def tenant() -> Tenant:
    """Cria um tenant simples para testes de throttle global."""
    tenant = Tenant(schema_name="acme", name="ACME Ltd.")
    tenant.save()
    Domain.objects.create(domain="acme.localhost", tenant=tenant, is_primary=True)
    return tenant


@pytest.mark.django_db
def test_anon_throttling(client, settings, tenant):
    """Throttle anônimo deve limitar requisições gerais."""
    rates = settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"].copy()
    rates["anon"] = "2/min"
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = rates

    url = "/_example"
    host = tenant.domains.first().domain
    for _ in range(2):
        client.get(url, HTTP_HOST=host)

    resp = client.get(url, HTTP_HOST=host)
    assert resp.status_code == 429
