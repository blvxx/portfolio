import hashlib
import hmac
import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import Base, WEBHOOK_SECRET, app, get_db

TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=TEST_ENGINE, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=TEST_ENGINE)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=TEST_ENGINE)
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield


def create_payment(reference="ORDER-1001"):
    response = client.post(
        "/payments",
        json={"customer_reference": reference, "amount_minor": 159900, "currency": "RUB"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def signed_headers(payload):
    body = json.dumps(payload, separators=(",", ":")).encode()
    signature = hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()
    return body, {"Content-Type": "application/json", "X-Signature": f"sha256={signature}"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_database_readiness_check():
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready", "database": "ok"}


def test_database_readiness_returns_503_when_database_is_unavailable():
    from sqlalchemy.exc import OperationalError

    class UnavailableSession:
        def execute(self, statement):
            raise OperationalError("SELECT 1", {}, Exception("database offline"))

        def close(self):
            pass

    def unavailable_db():
        yield UnavailableSession()

    app.dependency_overrides[get_db] = unavailable_db
    try:
        response = client.get("/health/ready")
        assert response.status_code == 503
        assert response.json()["detail"] == "Database unavailable"
    finally:
        app.dependency_overrides[get_db] = override_get_db


def test_create_and_get_payment():
    payment_id = create_payment()
    fetched = client.get(f"/payments/{payment_id}")
    assert fetched.status_code == 200
    assert fetched.json()["customer_reference"] == "ORDER-1001"


def test_reject_invalid_amount():
    response = client.post(
        "/payments",
        json={"customer_reference": "ORDER-1002", "amount_minor": 0, "currency": "RUB"},
    )
    assert response.status_code == 422


def test_unknown_payment_returns_404():
    response = client.get("/payments/99999")
    assert response.status_code == 404


def test_valid_status_transition():
    payment_id = create_payment("ORDER-1003")
    updated = client.patch(f"/payments/{payment_id}/status", json={"status": "paid"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "paid"


def test_terminal_status_cannot_be_changed():
    payment_id = create_payment("ORDER-1004")
    client.patch(f"/payments/{payment_id}/status", json={"status": "paid"})
    response = client.patch(f"/payments/{payment_id}/status", json={"status": "failed"})
    assert response.status_code == 409


def test_webhook_updates_payment_with_valid_signature():
    payment_id = create_payment("ORDER-WH-1")
    payload = {"event_id": "evt-1001", "payment_id": payment_id, "status": "paid"}
    body, headers = signed_headers(payload)
    response = client.post("/webhooks/payment-status", content=body, headers=headers)
    assert response.status_code == 200
    assert response.json()["duplicate"] is False
    assert client.get(f"/payments/{payment_id}").json()["status"] == "paid"


def test_webhook_rejects_invalid_signature():
    payment_id = create_payment("ORDER-WH-2")
    payload = {"event_id": "evt-1002", "payment_id": payment_id, "status": "paid"}
    body = json.dumps(payload).encode()
    response = client.post(
        "/webhooks/payment-status",
        content=body,
        headers={"X-Signature": "sha256=invalid"},
    )
    assert response.status_code == 401
    assert client.get(f"/payments/{payment_id}").json()["status"] == "pending"


def test_webhook_is_idempotent_for_same_event_and_payload():
    payment_id = create_payment("ORDER-WH-3")
    payload = {"event_id": "evt-1003", "payment_id": payment_id, "status": "paid"}
    body, headers = signed_headers(payload)
    first = client.post("/webhooks/payment-status", content=body, headers=headers)
    second = client.post("/webhooks/payment-status", content=body, headers=headers)
    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json()["duplicate"] is True


def test_webhook_rejects_reused_event_id_with_different_payload():
    payment_id = create_payment("ORDER-WH-4")
    first_payload = {"event_id": "evt-1004", "payment_id": payment_id, "status": "paid"}
    first_body, first_headers = signed_headers(first_payload)
    assert client.post("/webhooks/payment-status", content=first_body, headers=first_headers).status_code == 200

    second_payload = {"event_id": "evt-1004", "payment_id": payment_id, "status": "failed"}
    second_body, second_headers = signed_headers(second_payload)
    response = client.post("/webhooks/payment-status", content=second_body, headers=second_headers)
    assert response.status_code == 409
