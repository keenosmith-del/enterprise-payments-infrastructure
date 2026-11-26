from fastapi.testclient import TestClient

from packages.epi_foundation.app import Settings, create_app


def test_liveness_does_not_require_database() -> None:
    client = TestClient(create_app("test", Settings(database_url="")))
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "live"}
    assert response.headers["x-request-id"]


def test_readiness_fails_closed_without_database() -> None:
    client = TestClient(create_app("test", Settings(database_url="")))
    response = client.get("/health/ready")
    assert response.status_code == 503
    assert response.json() == {"status": "not_ready"}


def test_info_identifies_application() -> None:
    client = TestClient(create_app("test", Settings(database_url="")))
    assert client.get("/info").json()["application"] == "test"


def test_correlation_id_is_validated() -> None:
    client = TestClient(create_app("test", Settings(database_url="")))
    correlation = "10000000-0000-4000-8000-000000000001"
    response = client.get("/health/live", headers={"X-Correlation-ID": correlation})
    assert response.headers["X-Correlation-ID"] == correlation
    response = client.get("/health/live", headers={"X-Correlation-ID": "untrusted-value"})
    assert response.headers["X-Correlation-ID"] == response.headers["X-Request-ID"]


def test_protected_endpoint_requires_credentials() -> None:
    client = TestClient(create_app("test", Settings(database_url="")))
    response = client.get("/tenants/10000000-0000-4000-8000-000000000001/legal-entities")
    assert response.status_code == 401
    assert response.json()["error"] == "request_failed"


def test_unconfigured_identity_fails_closed() -> None:
    client = TestClient(create_app("test", Settings(database_url="")))
    response = client.get("/tenants/10000000-0000-4000-8000-000000000001/legal-entities", headers={"Authorization": "Bearer untrusted"})
    assert response.status_code == 503
