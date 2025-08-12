"""
Example ViewSet com RBAC para testes
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.api.permissions import IsTenantMember
from sample.models import SampleModel
from sample.api import SampleSerializer


class ExampleRBACViewSet(viewsets.ModelViewSet):
    """ViewSet de exemplo com RBAC para testes"""
    queryset = SampleModel.objects.all()
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticated, IsTenantMember]
    
    def get_queryset(self):
        # Filtra apenas objetos do tenant atual
        return self.queryset.filter(tenant=getattr(self.request, 'tenant', None))
    
    def perform_create(self, serializer):
        # Associa o objeto ao tenant atual
        serializer.save(tenant=getattr(self.request, 'tenant', None))
