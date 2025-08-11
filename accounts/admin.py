from django.contrib import admin

from accounts.models import Membership, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin básico para usuários."""

    list_display = ("username", "email", "is_staff")


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    """Admin para gerenciar associações de papéis por tenant."""

    list_display = ("user", "tenant", "role", "created_at")
    list_filter = ("role",)
