"""Permissões reutilizáveis para o projeto."""

from typing import Iterable

from rest_framework.permissions import BasePermission

from accounts.roles import Role
from accounts.services import get_user_role


class HasRole(BasePermission):
    """Verifica se o usuário possui um dos papéis permitidos."""

    allowed_roles: Iterable[str] = ()

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            self.message = "Autenticação requerida."
            return False

        role = get_user_role(request.user, getattr(request, "tenant", None))
        if role is None:
            self.message = "Usuário sem associação neste tenant."
            return False

        if role.value in self.allowed_roles:
            return True

        roles_txt = ", ".join(self.allowed_roles)
        self.message = f"Você não tem permissão para esta ação (papel: {roles_txt} requerido)."
        return False


class IsAdmin(HasRole):
    """Permite apenas usuários com papel de administrador."""

    allowed_roles = (Role.ADMIN.value,)


class IsTechnician(HasRole):
    """Permite apenas usuários com papel de técnico."""

    allowed_roles = (Role.TECHNICIAN.value,)


class IsRequester(HasRole):
    """Permite apenas usuários com papel de solicitante."""

    allowed_roles = (Role.REQUESTER.value,)


class DenyAll(BasePermission):
    """Permissão utilitária que bloqueia qualquer acesso."""

    def has_permission(self, request, view):  # pragma: no cover - trivial
        return False


class IsOwnerOrAdmin(BasePermission):
    """Permite apenas se o objeto foi criado pelo usuário ou se ele é admin."""

    def has_object_permission(self, request, view, obj):
        role = get_user_role(request.user, getattr(request, "tenant", None))
        if role == Role.ADMIN:
            return True
        return getattr(obj, "created_by_id", None) == request.user.id


class IsAssigneeOrAdmin(BasePermission):
    """Permite apenas o responsável ou administrador."""

    def has_object_permission(self, request, view, obj):
        role = get_user_role(request.user, getattr(request, "tenant", None))
        if role == Role.ADMIN:
            return True
        return getattr(obj, "assignee_id", None) == request.user.id


class IsRequesterSelfOrAdmin(BasePermission):
    """Permite somente o solicitante do objeto ou administrador."""

    def has_object_permission(self, request, view, obj):
        role = get_user_role(request.user, getattr(request, "tenant", None))
        if role == Role.ADMIN:
            return True
        return getattr(obj, "requester_id", None) == request.user.id
