from rest_framework import serializers, viewsets

from accounts.roles import Role
from accounts.services import get_user_role
from core.mixins import OwnershipQuerysetMixin, RoleRequiredMixin, TenantScopedMixin
from core.permissions import IsOwnerOrAdmin
from sandbox.models import ExampleOwnedModel


class ExampleOwnedSerializer(serializers.ModelSerializer):
    """Serializador simples para o modelo de exemplo."""

    class Meta:
        model = ExampleOwnedModel
        fields = ["id", "name", "created_by", "assignee", "requester"]
        read_only_fields = ("id", "created_by")


class ExampleOwnedViewSet(RoleRequiredMixin, TenantScopedMixin, OwnershipQuerysetMixin, viewsets.ModelViewSet):
    """ViewSet que demonstra o uso das permissões e mixins."""

    queryset = ExampleOwnedModel.objects.all()
    serializer_class = ExampleOwnedSerializer
    required_roles_write = (Role.ADMIN.value, Role.REQUESTER.value)
    object_level_permissions = [IsOwnerOrAdmin]
    ownership_field = "created_by"
    assignee_field = "assignee"

    def get_queryset(self):
        qs = super().get_queryset()
        return self.filter_queryset_by_ownership(qs)

    def perform_create(self, serializer):
        role = get_user_role(self.request.user, self.request.tenant)
        data = {"tenant": self.request.tenant, "created_by": self.request.user}
        if role == Role.REQUESTER:
            data["requester"] = self.request.user
        serializer.save(**data)
