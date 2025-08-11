from typing import Optional

from accounts.models import Membership
from accounts.roles import Role


def get_user_role(user, tenant) -> Optional[Role]:
    """Obtém o papel do usuário para um tenant específico."""

    try:
        membership = Membership.objects.get(user=user, tenant=tenant)
        return Role(membership.role)
    except Membership.DoesNotExist:
        return None


def user_has_role(user, tenant, role: Role) -> bool:
    """Verifica se o usuário possui um determinado papel no tenant."""

    return get_user_role(user, tenant) == role
