from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.roles import ROLE_CHOICES, Role


class User(AbstractUser):
    """Usuário base do sistema, derivado de AbstractUser."""

    # Nenhum campo adicional por enquanto, mas o modelo é personalizável
    pass


class Membership(models.Model):
    """Associação de um usuário a um tenant com determinado papel."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    tenant = models.ForeignKey("tenancy.Tenant", on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "tenant"], name="unique_membership"),
        ]

    def __str__(self) -> str:  # pragma: no cover - representação textual simples
        return f"{self.user} @ {self.tenant} ({self.role})"
