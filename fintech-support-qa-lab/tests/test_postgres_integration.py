import hashlib
import hmac
import json
import os
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import Base, WEBHOOK_SECRET, app, get_db

DATABASE_URL = os.getenv("TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(
    not DATABASE_URL,
    reason="Set TEST_DATABASE_URL to run PostgreSQL integration checks",
)


def test_payment_api_and_signed_webhook_use_postgres():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    reference = f"PG-{uuid.uuid4().hex[:12]}"
    try:
        with TestClient(app) as client:
            created = client.post(
                "/payments",
                json={
                    "customer_reference": reference,
                    "amount_minor": 12500,
                    "currency": "RUB",
                },
            )
            assert created.status_code == 201
            payment_id = created.json()["id"]
            assert created.json()["status"] == "pending"

            fetched = client.get(f"/payments/{payment_id}")
            assert fetched.status_code == 200
            assert fetched.json()["customer_reference"] == reference

            payload = {
                "event_id": f"evt-{uuid.uuid4().hex}",
                "payment_id": payment_id,
                "status": "paid",
            }
            body = json.dumps(payload, separators=(",", ":")).encode()
            signature = hmac.new(
                WEBHOOK_SECRET.encode(), body, hashlib.sha256
            ).hexdigest()
            webhook = client.post(
                "/webhooks/payment-status",
                content=body,
                headers={
                    "Content-Type": "application/json",
                    "X-Signature": f"sha256={signature}",
                },
            )
            assert webhook.status_code == 200
            assert webhook.json()["duplicate"] is False

            updated = client.get(f"/payments/{payment_id}")
            assert updated.status_code == 200
            assert updated.json()["status"] == "paid"
    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
