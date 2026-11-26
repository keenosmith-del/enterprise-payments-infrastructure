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
