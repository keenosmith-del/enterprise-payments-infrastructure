"""Real Keycloak-issued tokens; synthetic development identities only."""
import os

import pytest
from fastapi import HTTPException

from packages.epi_foundation.identity import OIDCVerifier
from scripts.m01.bootstrap_keycloak import APPS, token

ORIGIN = os.getenv("EPI_KEYCLOAK_ORIGIN", "http://127.0.0.1:8180")
ISSUER = ORIGIN + "/realms/epi"


@pytest.mark.parametrize("app", APPS)
def test_keycloak_issued_token_and_wrong_audience(app):
    access_token = token("synthetic-user", os.environ["EPI_KEYCLOAK_USER_PASSWORD"], app, "epi")
    verifier = OIDCVerifier(ISSUER, app, ISSUER + "/protocol/openid-connect/certs")
    principal = verifier.verify(access_token)
    assert principal.kind == "human"
    assert "foundation-reader" in principal.roles
    assert "foundation.read" in principal.scopes
    assert len(principal.tenants) == 1
    wrong = OIDCVerifier(ISSUER, "not-this-app", ISSUER + "/protocol/openid-connect/certs")
    with pytest.raises(HTTPException) as error:
        wrong.verify(access_token)
    assert error.value.status_code == 401
