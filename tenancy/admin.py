from django.contrib import admin

from .models import Tenant, Domain


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    """Administração básica do tenant."""
    list_display = ("schema_name", "name", "plan", "created_at")
    search_fields = ("schema_name", "name")


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    """Administração dos domínios associados aos tenants."""
    list_display = ("domain", "tenant", "is_primary")
    list_filter = ("is_primary",)
    search_fields = ("domain",)
