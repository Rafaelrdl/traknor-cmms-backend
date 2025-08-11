from django.http import JsonResponse
from django.db import connection


def health(request):
    """Endpoint simples para verificar o schema atual."""
    return JsonResponse({"status": "ok", "schema": connection.schema_name})
