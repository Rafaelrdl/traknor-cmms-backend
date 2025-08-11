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

    # Escopo de throttling dedicado para evitar brute-force
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth_login"

    def post(self, request):  # pragma: no cover - implementação será feita em outra issue
        """Endpoint de login ainda não implementado."""
        return Response({"detail": "Login não implementado"}, status=501)
