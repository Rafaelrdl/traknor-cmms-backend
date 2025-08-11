from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.services import get_user_role

User = get_user_model()


class MeSerializer(serializers.ModelSerializer):
    """Serializador para retornar os dados do próprio usuário.

    Comentários explicativos em PT-BR conforme instruções.
    """

    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
        ]

    def get_role(self, obj: User) -> str | None:
        """Obtém o papel do usuário no tenant atual."""
        request = self.context.get("request")
        if not request:
            return None
        tenant = getattr(request, "tenant", None)
        if not tenant:
            return None
        role = get_user_role(obj, tenant)
        return role.value if role else None
