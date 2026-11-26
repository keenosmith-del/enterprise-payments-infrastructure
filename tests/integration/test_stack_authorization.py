"""Exercise signed Keycloak tokens against actual running backend and database."""
import json
import os
import urllib.error
import urllib.request

import pytest
from scripts.m01.bootstrap_keycloak import request, token

APPS = (("policy-administration", 8001), ("payments-hub", 8002),
        ("banking-simulator", 8003), ("payroll-simulator", 8004))
TENANT_A = "10000000-0000-4000-8000-000000000001"
TENANT_B = "10000000-0000-4000-8000-000000000002"


def get(port, path, access_token=None):
    headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}
    request = urllib.request.Request(f"http://127.0.0.1:{port}{path}", headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, json.load(error)


@pytest.mark.parametrize("app,port", APPS)
def test_authenticated_tenant_boundary(app, port):
    access = token("synthetic-user", os.environ["EPI_KEYCLOAK_USER_PASSWORD"], app, "epi")
    assert get(port, f"/tenants/{TENANT_A}/legal-entities")[0] == 401
    assert get(port, f"/tenants/{TENANT_A}/legal-entities", "invalid-token")[0] == 401
    status, data = get(port, f"/tenants/{TENANT_A}/legal-entities", access)
    assert status == 200
    assert [item["name"] for item in data["items"]] == ["Synthetic Entity A"]
    assert get(port, f"/tenants/{TENANT_B}/legal-entities", access)[0] == 403
    limited = token("synthetic-limited", os.environ["EPI_KEYCLOAK_LIMITED_PASSWORD"], app, "epi")
    assert get(port, f"/tenants/{TENANT_A}/legal-entities", limited)[0] == 403
    wrong = token("synthetic-user", os.environ["EPI_KEYCLOAK_USER_PASSWORD"], ("payments-hub" if app != "payments-hub" else "policy-administration"), "epi")
    assert get(port, f"/tenants/{TENANT_A}/legal-entities", wrong)[0] == 401


def test_service_identity_cannot_impersonate_human():
    service = request("/realms/epi/protocol/openid-connect/token", {
        "grant_type": "client_credentials", "client_id": "integration-service",
        "client_secret": os.environ["EPI_KEYCLOAK_SERVICE_SECRET"]}, form=True)["access_token"]
    assert get(8002, f"/tenants/{TENANT_A}/legal-entities", service)[0] == 403
