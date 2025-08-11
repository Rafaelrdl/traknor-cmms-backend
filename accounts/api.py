"""Views relacionadas a contas de usuário."""

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MeSerializer


class MeView(APIView):
    """Retorna o perfil do usuário autenticado."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Responde com os dados do próprio usuário."""
        serializer = MeSerializer(request.user, context={"request": request})
        return Response({"data": serializer.data})
