from datetime import date, timedelta
import pytest
from fastapi.testclient import TestClient
from app import app, bookings, idempotency

@pytest.fixture
def client():
    bookings.clear()
    idempotency.clear()
    return TestClient(app)

def payload(**overrides):
    body = {
        "room_id": "room-101",
        "start_date": "2027-03-12",
        "end_date": "2027-03-15",
        "guests": 2,
        "guest": {"name": "Test Guest", "email": "qa@example.test"},
    }
    body.update(overrides)
    return body

AUTH = {"Authorization": "Bearer user-a"}

def test_rooms_pagination_contract(client):
    r = client.get("/v1/rooms?page=1&limit=1")
    assert r.status_code == 200
    assert len(r.json()["items"]) == 1
    assert r.json()["total"] == 2

def test_invalid_pagination_rejected(client):
    assert client.get("/v1/rooms?page=0").status_code == 400

def test_availability_reversed_dates_rejected(client):
    r = client.get("/v1/availability", params={"room_id":"room-101","start_date":"2027-03-15","end_date":"2027-03-12"})
    assert r.status_code == 400

def test_unknown_room_availability_returns_404(client):
    r = client.get("/v1/availability", params={"room_id":"ghost","start_date":"2027-03-12","end_date":"2027-03-15"})
    assert r.status_code == 404

def test_create_booking_returns_201_and_contract_fields(client):
    r = client.post("/v1/bookings", json=payload(), headers=AUTH)
    assert r.status_code == 201
    assert {"id","room_id","start_date","end_date","status"} <= set(r.json())
    assert r.json()["status"] == "confirmed"

def test_create_booking_requires_auth(client):
    assert client.post("/v1/bookings", json=payload()).status_code == 401

def test_invalid_date_range_rejected(client):
    r = client.post("/v1/bookings", json=payload(start_date="2027-03-16"))
    assert r.status_code == 400

def test_guest_capacity_validation(client):
    r = client.post("/v1/bookings", json=payload(guests=3))
    assert r.status_code == 400

def test_overlapping_booking_returns_conflict(client):
    first = client.post("/v1/bookings", json=payload(), headers={**AUTH, "Idempotency-Key":"key-1"})
    second = client.post("/v1/bookings", json=payload(start_date="2027-03-14", end_date="2027-03-17"), headers={**AUTH, "Idempotency-Key":"key-2"})
    assert first.status_code == 201
    assert second.status_code == 409
    assert len(bookings) == 1

def test_idempotent_retry_returns_same_booking(client):
    headers = {**AUTH, "Idempotency-Key":"retry-123"}
    first = client.post("/v1/bookings", json=payload(), headers=headers)
    second = client.post("/v1/bookings", json=payload(), headers=headers)
    assert first.status_code == second.status_code == 201
    assert first.json()["id"] == second.json()["id"]
    assert len(bookings) == 1

def test_idempotency_key_payload_mismatch_conflict(client):
    headers = {**AUTH, "Idempotency-Key":"same-key"}
    client.post("/v1/bookings", json=payload(), headers=headers)
    changed = client.post("/v1/bookings", json=payload(guests=1), headers=headers)
    assert changed.status_code == 409

def test_booking_owner_can_read(client):
    created = client.post("/v1/bookings", json=payload(), headers=AUTH)
    r = client.get(f"/v1/bookings/{created.json()['id']}", headers=AUTH)
    assert r.status_code == 200

def test_other_user_cannot_read_booking(client):
    created = client.post("/v1/bookings", json=payload(), headers=AUTH)
    r = client.get(f"/v1/bookings/{created.json()['id']}", headers={"Authorization":"Bearer user-b"})
    assert r.status_code == 404
    assert "guest" not in r.json()

def test_cancel_booking_and_idempotent_cancel(client):
    created = client.post("/v1/bookings", json=payload(), headers=AUTH)
    booking_id = created.json()["id"]
    first = client.delete(f"/v1/bookings/{booking_id}", headers=AUTH)
    second = client.delete(f"/v1/bookings/{booking_id}", headers=AUTH)
    assert first.status_code == second.status_code == 200
    assert first.json()["status"] == second.json()["status"] == "cancelled"

def test_cancel_missing_booking_returns_404(client):
    assert client.delete("/v1/bookings/nope", headers=AUTH).status_code == 404
