"""
Permissions customizadas para RBAC e multi-tenancy
"""
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, NotAuthenticated


class IsTenantMember(BasePermission):
    """Verifica se o usuário é membro do tenant atual"""
    message = "Tenant membership required."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated()
            
        # Verificar se o usuário tem membership no tenant atual
        if not getattr(request.user, "is_member_of_current_tenant", False):
            raise PermissionDenied(self.message)
            
        return True


class IsAdminRole(BasePermission):
    """Verifica se o usuário tem role de admin"""
    message = "Admin role required."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated()
            
        if getattr(request.user, "role", None) != "admin":
            raise PermissionDenied(self.message)
            
        return True


class IsTechnicianRole(BasePermission):
    """Verifica se o usuário tem role de técnico ou admin"""
    message = "Technician role or higher required."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated()
            
        role = getattr(request.user, "role", None)
        if role not in ["technician", "admin"]:
            raise PermissionDenied(self.message)
            
        return True
