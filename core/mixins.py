"""Mixins auxiliares para views DRF."""

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from accounts.roles import Role
from accounts.services import get_user_role
from core.permissions import HasRole


class RoleRequiredMixin:
    """Adiciona verificação de papéis conforme método HTTP."""

    required_roles_read = (Role.ADMIN.value, Role.TECHNICIAN.value, Role.REQUESTER.value)
    required_roles_write = (Role.ADMIN.value,)
    object_level_permissions = ()

    def get_permissions(self):
        perms = [IsAuthenticated()]
        roles = (
            self.required_roles_read if self.request.method in SAFE_METHODS else self.required_roles_write
        )
        role_perm = HasRole()
        role_perm.allowed_roles = roles
        perms.append(role_perm)
        perms.extend(p() for p in self.object_level_permissions)
        return perms


class OwnershipQuerysetMixin:
    """Filtra o queryset de acordo com a propriedade do objeto."""

    ownership_field = "created_by"
    assignee_field = "assignee"
    requester_field = "requester"

    def filter_queryset_by_ownership(self, qs):
        role = get_user_role(self.request.user, getattr(self.request, "tenant", None))
        if role == Role.ADMIN:
            return qs
        if role == Role.TECHNICIAN:
            q = Q(**{self.assignee_field: self.request.user}) | Q(
                **{self.ownership_field: self.request.user}
            )
            return qs.filter(q)
        if role == Role.REQUESTER:
            return qs.filter(**{self.ownership_field: self.request.user})
        return qs.none()


class TenantScopedMixin:
    """Garante que o queryset esteja limitado ao tenant atual."""

    def get_queryset(self):  # pragma: no cover - comportamento simples
        qs = super().get_queryset()
        tenant = getattr(self.request, "tenant", None)
        if hasattr(qs.model, "tenant_id"):
            return qs.filter(tenant=tenant)
        return qs
