import pytest
from rest_framework.authtoken.models import Token

from accounts.models import Membership, User
from accounts.roles import Role
from sandbox.models import ExampleOwnedModel
from tenancy.models import Domain, Tenant
from django_tenants.utils import schema_context


@pytest.fixture
def tenant(db):
    """Cria tenant básico para os testes de RBAC."""
    tenant = Tenant(schema_name="acme", name="ACME")
    tenant.save()
    Domain.objects.create(domain="acme.localhost", tenant=tenant, is_primary=True)
    return tenant


@pytest.fixture
def users(tenant):
    """Cria usuários com papéis distintos."""

    def make(username: str, role: Role):
        user = User.objects.create_user(username=username, password="pass")
        Membership.objects.create(user=user, tenant=tenant, role=role.value)
        token = Token.objects.create(user=user)
        return {"user": user, "token": token}

    return {
        "admin": make("admin", Role.ADMIN),
        "tech": make("tech", Role.TECHNICIAN),
        "req": make("req", Role.REQUESTER),
    }


@pytest.fixture
def examples(tenant, users):
    """Cria objetos de exemplo para validação de ownership."""
    admin = users["admin"]["user"]
    tech = users["tech"]["user"]
    req = users["req"]["user"]
    with schema_context(tenant.schema_name):
        e1 = ExampleOwnedModel.objects.create(
            tenant=tenant, name="a1", created_by=admin, assignee=tech, requester=req
        )
        e2 = ExampleOwnedModel.objects.create(
            tenant=tenant, name="t1", created_by=tech, assignee=tech, requester=req
        )
        e3 = ExampleOwnedModel.objects.create(
            tenant=tenant, name="r1", created_by=req, assignee=tech, requester=req
        )
    return e1, e2, e3


def auth_headers(token):
    return {"HTTP_AUTHORIZATION": f"Token {token.key}", "HTTP_HOST": "acme.localhost"}


@pytest.mark.django_db
def test_authentication_required(client, tenant):
    resp = client.get("/sandbox/examples/", HTTP_HOST="acme.localhost")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_membership_required(client, tenant):
    user = User.objects.create_user(username="nomem", password="pass")
    token = Token.objects.create(user=user)
    resp = client.get("/sandbox/examples/", **auth_headers(token))
    assert resp.status_code == 403
    assert "associação" in resp.json()["detail"]


@pytest.mark.django_db
def test_list_permissions(client, tenant, users, examples):
    admin_resp = client.get("/sandbox/examples/", **auth_headers(users["admin"]["token"]))
    assert len(admin_resp.json()["data"]) == 3

    tech_resp = client.get("/sandbox/examples/", **auth_headers(users["tech"]["token"]))
    assert len(tech_resp.json()["data"]) == 2

    req_resp = client.get("/sandbox/examples/", **auth_headers(users["req"]["token"]))
    assert len(req_resp.json()["data"]) == 1


@pytest.mark.django_db
def test_retrieve_permissions(client, tenant, users, examples):
    e1, e2, e3 = examples
    tech_token = users["tech"]["token"]
    req_token = users["req"]["token"]

    ok1 = client.get(f"/sandbox/examples/{e1.id}/", **auth_headers(tech_token))
    assert ok1.status_code == 200

    forbidden = client.get(f"/sandbox/examples/{e3.id}/", **auth_headers(tech_token))
    assert forbidden.status_code == 403

    ok_req = client.get(f"/sandbox/examples/{e3.id}/", **auth_headers(req_token))
    assert ok_req.status_code == 200

    req_forbidden = client.get(f"/sandbox/examples/{e1.id}/", **auth_headers(req_token))
    assert req_forbidden.status_code == 403


@pytest.mark.django_db
def test_create_permissions(client, tenant, users):
    data = {"name": "novo", "assignee": users["tech"]["user"].id, "requester": users["req"]["user"].id}

    admin_resp = client.post(
        "/sandbox/examples/",
        data,
        content_type="application/json",
        **auth_headers(users["admin"]["token"]),
    )
    assert admin_resp.status_code == 201

    tech_resp = client.post(
        "/sandbox/examples/",
        data,
        content_type="application/json",
        **auth_headers(users["tech"]["token"]),
    )
    assert tech_resp.status_code == 403

    req_resp = client.post(
        "/sandbox/examples/",
        {"name": "mine"},
        content_type="application/json",
        **auth_headers(users["req"]["token"]),
    )
    assert req_resp.status_code == 201
    assert req_resp.json()["data"]["created_by"] == users["req"]["user"].id


@pytest.mark.django_db
def test_update_and_delete_permissions(client, tenant, users, examples):
    e1, e2, e3 = examples
    tech_token = users["tech"]["token"]
    req_token = users["req"]["token"]
    admin_token = users["admin"]["token"]

    tech_update = client.patch(
        f"/sandbox/examples/{e1.id}/",
        {"name": "x"},
        content_type="application/json",
        **auth_headers(tech_token),
    )
    assert tech_update.status_code == 200

    req_update = client.patch(
        f"/sandbox/examples/{e3.id}/",
        {"name": "y"},
        content_type="application/json",
        **auth_headers(req_token),
    )
    assert req_update.status_code == 403

    delete_forbidden = client.delete(f"/sandbox/examples/{e2.id}/", **auth_headers(tech_token))
    assert delete_forbidden.status_code == 403

    delete_admin = client.delete(f"/sandbox/examples/{e2.id}/", **auth_headers(admin_token))
    assert delete_admin.status_code == 204


@pytest.mark.django_db
def test_membership_other_tenant_denied(client, tenant, users):
    other = Tenant(schema_name="oth", name="Other")
    other.save()
    Domain.objects.create(domain="oth.localhost", tenant=other, is_primary=True)
    outsider = User.objects.create_user(username="outsider", password="pass")
    Membership.objects.create(user=outsider, tenant=other, role=Role.TECHNICIAN.value)
    token = Token.objects.create(user=outsider)

    resp = client.get("/sandbox/examples/", **auth_headers(token))
    assert resp.status_code == 403
