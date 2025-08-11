from django.http import JsonResponse
from django.db import connection


def health(request):
    """Endpoint simples para verificar o schema atual."""
    return JsonResponse({"status": "ok", "schema": connection.schema_name})


def trigger_error(request):  # pragma: no cover - usado apenas em testes manuais
    """View que dispara uma exceção para validar o handler de erros."""
    raise Exception("Erro forçado")
