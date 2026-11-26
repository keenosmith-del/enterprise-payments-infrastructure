"""Cryptographic unit checks; these do not substitute for Keycloak integration."""
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import Mock

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import HTTPException

from packages.epi_foundation.identity import OIDCVerifier


@pytest.fixture
def signed_tokens():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    verifier = OIDCVerifier("https://identity.example/realms/epi", "payments-hub", "https://identity.example/jwks")
    verifier.keys.get_signing_key_from_jwt = Mock(return_value=SimpleNamespace(key=key.public_key()))
    base = {"iss": verifier.issuer, "aud": verifier.audience, "sub": "synthetic",
            "iat": datetime.now(timezone.utc), "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            "tenant_ids": ["10000000-0000-4000-8000-000000000001"],
            "legal_entity_ids": ["20000000-0000-4000-8000-000000000001"], "principal_kind": "human",
            "realm_access": {"roles": ["foundation-reader"]}, "scope": "foundation.read"}
    return verifier, key, base


def test_valid_signature_and_claims(signed_tokens):
    verifier, key, claims = signed_tokens
    principal = verifier.verify(jwt.encode(claims, key, algorithm="RS256"))
    assert principal.kind == "human"
    assert len(principal.tenants) == 1
    assert "foundation-reader" in principal.roles


@pytest.mark.parametrize("field,value", [("iss", "https://wrong"), ("aud", "wrong"),
                                      ("exp", datetime.now(timezone.utc) - timedelta(minutes=1)),
                                      ("principal_kind", "untrusted")])
def test_invalid_claims_rejected(signed_tokens, field, value):
    verifier, key, claims = signed_tokens
    claims[field] = value
    with pytest.raises(HTTPException) as exc:
        verifier.verify(jwt.encode(claims, key, algorithm="RS256"))
    assert exc.value.status_code == 401


def test_invalid_signature_rejected(signed_tokens):
    verifier, _, claims = signed_tokens
    other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with pytest.raises(HTTPException) as exc:
        verifier.verify(jwt.encode(claims, other, algorithm="RS256"))
    assert exc.value.status_code == 401
