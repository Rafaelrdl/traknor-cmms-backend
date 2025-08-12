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
def test_cors_preflight_allowed(tenant_client, tenant):
    """Origem permitida deve receber todos os headers de CORS."""
    resp = _preflight(tenant_client, "/health", "http://localhost:5173")
    assert resp.status_code in {200, 204}
    assert resp["Access-Control-Allow-Origin"] == "http://localhost:5173"
    assert "GET" in resp["Access-Control-Allow-Methods"]
    # Verificação case-insensitive para authorization header
    headers = resp["Access-Control-Allow-Headers"].lower()
    assert "authorization" in headers
    assert resp["Access-Control-Allow-Credentials"] == "true"
    assert resp["Access-Control-Max-Age"] == "600"


@pytest.mark.django_db
def test_cors_preflight_blocked(tenant_client, tenant):
    """Origem não listada não deve receber headers CORS."""
    resp = _preflight(tenant_client, "/health", "http://malicioso.com")
    assert resp.status_code in {200, 204}
    assert "Access-Control-Allow-Origin" not in resp.headers


@pytest.mark.django_db
def test_login_throttling(tenant_client, tenant, settings):
    """Excesso de tentativas de login deve retornar 429."""
    # Limpa cache de throttling para isolar teste
    from django.core.cache import cache
    cache.clear()
    
    # Reduz o limite para acelerar o teste
    rates = settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"].copy()
    rates["login"] = "2/min"
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = rates

    url = reverse("auth-login")
    for _ in range(2):
        tenant_client.post(url)

    resp = tenant_client.post(url)
    assert resp.status_code == 429
    body = resp.json()
    # Aceita qualquer formato que contenha os dados necessários
    if "status" in body:
        assert body["status"] == 429
        assert body["title"] == "Too Many Requests"
    elif "data" in body and "detail" in body["data"]:
        assert "throttled" in body["data"]["detail"].lower()
    else:
        assert False, f"Formato de resposta não reconhecido: {body}"


@pytest.mark.django_db
def test_anon_throttling(tenant_client, tenant, settings):
    """Throttle anônimo deve limitar requisições gerais."""
    # Limpa cache de throttling para isolar teste
    from django.core.cache import cache
    cache.clear()
    
    rates = settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"].copy()
    rates["anon"] = "2/min"
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = rates

    url = "/anon-throttle"
    for _ in range(2):
        tenant_client.get(url)

    resp = tenant_client.get(url)
    assert resp.status_code == 429
