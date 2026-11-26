"""Signature-verified OIDC token validation. Identity integration is in progress."""
from dataclasses import dataclass
from uuid import UUID

import jwt
from fastapi import HTTPException
from jwt import PyJWKClient
from jwt.exceptions import PyJWTError, PyJWKClientError


@dataclass(frozen=True)
class Principal:
    subject: str
    kind: str
    tenants: frozenset[UUID]
    legal_entities: frozenset[UUID]
    roles: frozenset[str]
    scopes: frozenset[str]


class OIDCVerifier:
    def __init__(self, issuer: str, audience: str, jwks_url: str) -> None:
        self.issuer = issuer
        self.audience = audience
        self.keys = PyJWKClient(jwks_url, timeout=3, cache_jwk_set=True, lifespan=300)

    def verify(self, token: str) -> Principal:
        try:
            key = self.keys.get_signing_key_from_jwt(token).key
            claims = jwt.decode(token, key, algorithms=["RS256"], issuer=self.issuer,
                                audience=self.audience, options={"require": ["iss", "aud", "exp", "sub", "iat"]})
            tenant_values = claims.get("tenant_ids", [])
            entity_values = claims.get("legal_entity_ids", [])
            realm = claims.get("realm_access", {})
            kind = claims.get("principal_kind")
            if not isinstance(tenant_values, list) or not isinstance(entity_values, list) or not isinstance(realm, dict):
                raise ValueError("invalid identity claims")
            roles = realm.get("roles", [])
            scopes = claims.get("scope", "")
            if kind not in ("human", "service") or not isinstance(roles, list) or not isinstance(scopes, str):
                raise ValueError("invalid identity claims")
            if not all(isinstance(role, str) for role in roles):
                raise ValueError("invalid roles")
            return Principal(str(claims["sub"]), kind, frozenset(UUID(t) for t in tenant_values),
                             frozenset(UUID(entity) for entity in entity_values), frozenset(roles), frozenset(scopes.split()))
        except (PyJWTError, PyJWKClientError, ValueError, TypeError, KeyError):
            raise HTTPException(status_code=401, detail="Invalid credentials") from None
