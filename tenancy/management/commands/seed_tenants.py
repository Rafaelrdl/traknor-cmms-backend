from django.core.management.base import BaseCommand
from django_tenants.utils import get_tenant_model, get_tenant_domain_model


class Command(BaseCommand):
    """Popula o banco com tenants de exemplo."""

    help = "Cria tenants de exemplo (acme, beta)"

    def handle(self, *args, **options):
        TenantModel = get_tenant_model()
        DomainModel = get_tenant_domain_model()

        examples = [
            ("acme", "ACME Ltd.", "acme.localhost"),
            ("beta", "Beta Ltd.", "beta.localhost"),
        ]

        for schema, name, domain in examples:
            if TenantModel.objects.filter(schema_name=schema).exists():
                self.stdout.write(f"Tenant {schema} já existe, pulando...")
                continue
            tenant = TenantModel(schema_name=schema, name=name)
            tenant.save()
            DomainModel.objects.create(domain=domain, tenant=tenant, is_primary=True)
            self.stdout.write(self.style.SUCCESS(f"Tenant {schema} criado"))
