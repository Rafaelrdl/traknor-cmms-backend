from django.conf import settings
from django.db import models


class ExampleOwnedModel(models.Model):
    """Modelo de exemplo para demonstrar permissões e ownership."""

    tenant = models.ForeignKey("tenancy.Tenant", on_delete=models.CASCADE, related_name="examples")
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_examples")
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_examples")
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="requested_examples")

    def __str__(self):  # pragma: no cover - representação simples
        return self.name
