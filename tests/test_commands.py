import pytest
from django.core.management import call_command

from tenancy.models import Tenant, Domain


@pytest.mark.django_db
def test_create_tenant_command():
    """Testa criação de tenant via comando de management."""
    call_command(
        "create_tenant",
        schema="gamma",
        name="Gamma Ltd.",
        domain="gamma.localhost",
        primary=True,
    )
    tenant = Tenant.objects.get(schema_name="gamma")
    assert tenant.name == "Gamma Ltd."
    assert Domain.objects.filter(domain="gamma.localhost", tenant=tenant).exists()
