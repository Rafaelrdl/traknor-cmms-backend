from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from accounts.models import Membership, User
from accounts.roles import Role
from tenancy.models import Tenant, Domain


class Command(BaseCommand):
    """Comando simples que cria dados de exemplo para RBAC."""

    help = "Cria tenant demo, usuários e seus respectivos tokens e memberships"

    def handle(self, *args, **options):  # pragma: no cover - usado em ambiente local
        tenant, _ = Tenant.objects.get_or_create(
            schema_name="demo",
            defaults={"name": "Demo"},
        )
        Domain.objects.get_or_create(domain="demo.localhost", tenant=tenant, is_primary=True)

        users = {
            Role.ADMIN: ("admin@demo", "admin"),
            Role.TECHNICIAN: ("tech@demo", "tech"),
            Role.REQUESTER: ("req@demo", "req"),
        }

        for role, (email, username) in users.items():
            user, _ = User.objects.get_or_create(username=username, defaults={"email": email})
            user.set_password("demo123")
            user.save()
            Membership.objects.get_or_create(user=user, tenant=tenant, role=role.value)
            token, _ = Token.objects.get_or_create(user=user)
            self.stdout.write(f"{role.value}: {token.key}")

        self.stdout.write(self.style.SUCCESS("Seeds de RBAC criadas com sucesso."))
