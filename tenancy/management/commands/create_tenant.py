from django.core.management.base import BaseCommand
from django_tenants.utils import get_tenant_model, get_tenant_domain_model


class Command(BaseCommand):
    """Comando para criar um tenant e seu domínio."""

    help = "Cria um novo tenant com domínio associado"

    def add_arguments(self, parser) -> None:
        parser.add_argument("--schema", required=True, help="Nome do schema do tenant")
        parser.add_argument("--name", required=True, help="Nome amigável do tenant")
        parser.add_argument("--domain", required=True, help="Domínio ou subdomínio para acessar o tenant")
        parser.add_argument("--primary", action="store_true", help="Define se o domínio é primário")

    def handle(self, *args, **options):
        TenantModel = get_tenant_model()
        DomainModel = get_tenant_domain_model()

        tenant = TenantModel(schema_name=options["schema"], name=options["name"])
        tenant.save()
        DomainModel.objects.create(
            domain=options["domain"],
            tenant=tenant,
            is_primary=options["primary"],
        )
        self.stdout.write(self.style.SUCCESS(f"Tenant {tenant.schema_name} criado com sucesso"))
