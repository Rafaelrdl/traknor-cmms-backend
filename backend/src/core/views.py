"""Views básicas da aplicação."""

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class HealthCheckView(APIView):
    """Retorna o status de saúde da API."""

    def get(self, request):
        """Responde com um simples JSON indicando que a API está funcionando."""
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
