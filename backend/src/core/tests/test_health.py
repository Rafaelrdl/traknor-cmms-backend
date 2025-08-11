"""Testes para o endpoint de saúde."""

from django.test import TestCase


class HealthCheckTests(TestCase):
    """Verifica se o endpoint /health responde corretamente."""

    def test_health_endpoint_returns_ok(self):
        """Deve retornar HTTP 200 com o JSON esperado."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
