import pytest
from django_tenants.utils import schema_context

from tenancy.models import Tenant, Domain
from sample.models import SampleModel


@pytest.mark.django_db
def test_data_isolation_between_schemas():
    """Garante que dados criados em um tenant não aparecem em outro."""
    with schema_context('public'):
        acme = Tenant(schema_name="acme", name="ACME Ltd.")
        acme.save()
        Domain.objects.create(domain="acme.localhost", tenant=acme, is_primary=True)

        beta = Tenant(schema_name="beta", name="Beta Ltd.")
        beta.save()
        Domain.objects.create(domain="beta.localhost", tenant=beta, is_primary=True)

    with schema_context("acme"):
        SampleModel.objects.create(name="item-acme")
        assert SampleModel.objects.count() == 1

    with schema_context("beta"):
        assert SampleModel.objects.count() == 0
