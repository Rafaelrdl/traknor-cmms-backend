from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny

from .models import SampleModel


class SampleSerializer(serializers.ModelSerializer):
    """Serializador simples para o modelo de exemplo."""

    class Meta:
        model = SampleModel
        fields = ["id", "name"]


class ExampleViewSet(viewsets.ModelViewSet):
    """ViewSet que expõe o modelo de exemplo para testes."""

    queryset = SampleModel.objects.all().order_by("id")
    serializer_class = SampleSerializer
    permission_classes = [AllowAny]
