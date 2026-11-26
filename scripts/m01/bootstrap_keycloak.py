"""Provision a synthetic development realm using disposable credentials from the environment."""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

ORIGIN = os.environ.get("EPI_KEYCLOAK_ORIGIN", "http://127.0.0.1:8180")
APPS = ("policy-administration", "payments-hub", "banking-simulator", "payroll-simulator")


def request(path: str, data: dict | None = None, token: str = "", method: str = "POST", form: bool = False):
    headers = {"Content-Type": "application/x-www-form-urlencoded" if form else "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = None if data is None else (urllib.parse.urlencode(data).encode() if form else json.dumps(data).encode())
    req = urllib.request.Request(ORIGIN + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            payload = response.read()
            return json.loads(payload) if payload else None
    except urllib.error.HTTPError as error:
        if error.code == 409 and method == "POST":
            return None
        try:
            detail = json.loads(error.read()).get("error", "unknown")
        except (ValueError, AttributeError):
            detail = "unknown"
        raise RuntimeError(f"Identity request failed: HTTP {error.code}, error={detail}, path={path}") from None


def token(username: str, password: str, client: str = "admin-cli", realm: str = "master") -> str:
    return request(f"/realms/{realm}/protocol/openid-connect/token", {
        "grant_type": "password", "client_id": client, "username": username, "password": password}, form=True)["access_token"]


def bootstrap() -> None:
    admin = token(os.environ["EPI_KEYCLOAK_ADMIN"], os.environ["EPI_KEYCLOAK_ADMIN_PASSWORD"])
    root = "/admin/realms/epi"
    request("/admin/realms", {"realm": "epi", "enabled": True, "accessTokenLifespan": 300,
                              "sslRequired": "none"}, admin)
    request(root + "/roles", {"name": "foundation-reader"}, admin)
    request(root + "/client-scopes", {"name": "foundation.read", "protocol": "openid-connect",
                                        "attributes": {"include.in.token.scope": "true"}}, admin)
    scopes = request(root + "/client-scopes", token=admin, method="GET")
    scope_id = next(scope["id"] for scope in scopes if scope["name"] == "foundation.read")
    for app in APPS:
        port = {"policy-administration": 5173, "payments-hub": 5174,
                "banking-simulator": 5175, "payroll-simulator": 5176}[app]
        mappers = [
            {"name": "audience", "protocol": "openid-connect", "protocolMapper": "oidc-audience-mapper",
             "config": {"included.custom.audience": app, "access.token.claim": "true", "id.token.claim": "false"}},
            {"name": "tenant-ids", "protocol": "openid-connect", "protocolMapper": "oidc-usermodel-attribute-mapper",
             "config": {"user.attribute": "tenant_ids", "claim.name": "tenant_ids", "jsonType.label": "String",
                        "multivalued": "true", "access.token.claim": "true"}},
            {"name": "entity-ids", "protocol": "openid-connect", "protocolMapper": "oidc-usermodel-attribute-mapper",
             "config": {"user.attribute": "legal_entity_ids", "claim.name": "legal_entity_ids", "jsonType.label": "String",
                        "multivalued": "true", "access.token.claim": "true"}},
            {"name": "principal-kind", "protocol": "openid-connect", "protocolMapper": "oidc-hardcoded-claim-mapper",
             "config": {"claim.name": "principal_kind", "claim.value": "human", "jsonType.label": "String", "access.token.claim": "true"}},
        ]
        request(root + "/clients", {"clientId": app, "enabled": True, "publicClient": True,
                 "standardFlowEnabled": True, "directAccessGrantsEnabled": True,
                 "attributes": {"pkce.code.challenge.method": "S256",
                                "post.logout.redirect.uris": f"http://127.0.0.1:{port}/*"},
                 "redirectUris": [f"http://127.0.0.1:{port}/*"], "webOrigins": [f"http://127.0.0.1:{port}"],
                 "protocolMappers": mappers}, admin)
        clients = request(root + "/clients?" + urllib.parse.urlencode({"clientId": app}), token=admin, method="GET")
        client_id = clients[0]["id"]
        existing_mappers = request(root + f"/clients/{client_id}/protocol-mappers/models", token=admin, method="GET")
        for mapper in mappers:
            if not any(existing.get("name") == mapper["name"] for existing in existing_mappers):
                request(root + f"/clients/{client_id}/protocol-mappers/models", mapper, admin)
        request(root + f"/clients/{client_id}/default-client-scopes/{scope_id}", {}, admin, method="PUT")
    # Test-only direct grant clients exercise scope denial and expiry against real tokens.
    negative_mappers = [dict(mapper) for mapper in mappers]
    negative_mappers[0] = {**negative_mappers[0], "config": {"included.custom.audience": "payments-hub", "access.token.claim": "true"}}
    for client_name, attributes in (("scope-negative", {}), ("expiry-test", {"access.token.lifespan": "1"})):
        request(root + "/clients", {"clientId": client_name, "enabled": True, "publicClient": True,
                "standardFlowEnabled": False, "directAccessGrantsEnabled": True,
                "attributes": attributes, "protocolMappers": negative_mappers}, admin)
    service_mappers = [
        {"name": "audience", "protocol": "openid-connect", "protocolMapper": "oidc-audience-mapper",
         "config": {"included.custom.audience": "payments-hub", "access.token.claim": "true"}},
        {"name": "principal-kind", "protocol": "openid-connect", "protocolMapper": "oidc-hardcoded-claim-mapper",
         "config": {"claim.name": "principal_kind", "claim.value": "service", "jsonType.label": "String", "access.token.claim": "true"}},
    ]
    request(root + "/clients", {"clientId": "integration-service", "enabled": True, "publicClient": False,
            "serviceAccountsEnabled": True, "standardFlowEnabled": False, "directAccessGrantsEnabled": False,
            "secret": os.environ["EPI_KEYCLOAK_SERVICE_SECRET"], "protocolMappers": service_mappers}, admin)
    service_clients = request(root + "/clients?clientId=integration-service", token=admin, method="GET")
    service_id = service_clients[0]["id"]
    service_client = request(root + f"/clients/{service_id}", token=admin, method="GET")
    service_client["secret"] = os.environ["EPI_KEYCLOAK_SERVICE_SECRET"]
    request(root + f"/clients/{service_id}", service_client, admin, method="PUT")
    profile = request(root + "/users/profile", token=admin, method="GET")
    changed = False
    for attribute_name in ("tenant_ids", "legal_entity_ids"):
        if not any(attribute.get("name") == attribute_name for attribute in profile["attributes"]):
            profile["attributes"].append({"name": attribute_name, "displayName": "Authorised scope",
                                          "multivalued": True, "permissions": {"view": ["admin"], "edit": ["admin"]}})
            changed = True
    if changed:
        request(root + "/users/profile", profile, admin, method="PUT")
    request(root + "/users", {"username": "synthetic-user", "enabled": True, "emailVerified": True,
            "firstName": "Synthetic", "lastName": "User", "email": "synthetic@example.invalid",
            "attributes": {"tenant_ids": ["10000000-0000-4000-8000-000000000001"],
                           "legal_entity_ids": ["20000000-0000-4000-8000-000000000001"]},
            "credentials": [{"type": "password", "value": os.environ["EPI_KEYCLOAK_USER_PASSWORD"], "temporary": False}]}, admin)
    request(root + "/users", {"username": "synthetic-limited", "enabled": True, "emailVerified": True,
            "firstName": "Synthetic", "lastName": "Limited", "email": "limited@example.invalid",
            "attributes": {"tenant_ids": ["10000000-0000-4000-8000-000000000001"],
                           "legal_entity_ids": ["20000000-0000-4000-8000-000000000001"]},
            "credentials": [{"type": "password", "value": os.environ["EPI_KEYCLOAK_LIMITED_PASSWORD"], "temporary": False}]}, admin)
    users = request(root + "/users?username=synthetic-user&exact=true", token=admin, method="GET")
    for username, password_name in (("synthetic-user", "EPI_KEYCLOAK_USER_PASSWORD"),
                                    ("synthetic-limited", "EPI_KEYCLOAK_LIMITED_PASSWORD")):
        entry = request(root + "/users?" + urllib.parse.urlencode({"username": username, "exact": "true"}), token=admin, method="GET")[0]
        entry["attributes"] = {"tenant_ids": ["10000000-0000-4000-8000-000000000001"],
                               "legal_entity_ids": ["20000000-0000-4000-8000-000000000001"]}
        request(root + f"/users/{entry['id']}", entry, admin, method="PUT")
        request(root + f"/users/{entry['id']}/reset-password",
                {"type": "password", "value": os.environ[password_name], "temporary": False}, admin, method="PUT")
    role = request(root + "/roles/foundation-reader", token=admin, method="GET")
    request(root + f"/users/{users[0]['id']}/role-mappings/realm", [role], admin)


if __name__ == "__main__":
    bootstrap()
