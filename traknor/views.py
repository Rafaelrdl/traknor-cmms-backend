from django.http import JsonResponse
from django.db import connection
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView


def health(request):
    """Endpoint simples para verificar o schema atual."""
    return JsonResponse({"status": "ok", "schema": connection.schema_name})


def trigger_error(request):  # pragma: no cover - usado apenas em testes manuais
    """View que dispara uma exceção para validar o handler de erros."""
    raise Exception("Erro forçado")


class LoginView(APIView):
    """View de login com proteção de rate limit."""

    # Configurações serão aplicadas no urls_tenant.py
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        """Endpoint de login para testes de throttling."""
        # Para testes, simula uma tentativa de login inválida
        return Response({"detail": "Invalid credentials"}, status=401)
