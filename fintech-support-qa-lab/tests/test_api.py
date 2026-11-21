import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import Base, app, get_db

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


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_payment():
    created = client.post(
        "/payments",
        json={"customer_reference": "ORDER-1001", "amount_minor": 159900, "currency": "RUB"},
    )
    assert created.status_code == 201
    payment_id = created.json()["id"]
    assert created.json()["status"] == "pending"

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
    created = client.post(
        "/payments",
        json={"customer_reference": "ORDER-1003", "amount_minor": 5000, "currency": "RUB"},
    )
    payment_id = created.json()["id"]

    updated = client.patch(f"/payments/{payment_id}/status", json={"status": "paid"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "paid"


def test_terminal_status_cannot_be_changed():
    created = client.post(
        "/payments",
        json={"customer_reference": "ORDER-1004", "amount_minor": 5000, "currency": "RUB"},
    )
    payment_id = created.json()["id"]
    client.patch(f"/payments/{payment_id}/status", json={"status": "paid"})

    response = client.patch(f"/payments/{payment_id}/status", json={"status": "failed"})
    assert response.status_code == 409
