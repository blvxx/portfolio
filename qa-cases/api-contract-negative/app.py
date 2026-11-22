"""Small fictional booking API used as a local QA target. No external services.""" 
from datetime import date
from typing import Optional
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Booking QA Sandbox", version="0.1.0")
rooms = {"room-101": {"capacity": 2}, "room-202": {"capacity": 4}}
bookings = {}
idempotency = {}

class Guest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str

class BookingRequest(BaseModel):
    room_id: str
    start_date: date
    end_date: date
    guests: int = Field(ge=1, le=8)
    guest: Guest

@app.get("/v1/rooms")
def list_rooms(page: int = 1, limit: int = 20):
    if page < 1 or limit < 1 or limit > 100:
        raise HTTPException(400, "page/limit out of range")
    items = list(rooms.items())
    start = (page - 1) * limit
    return {"items": [{"id": k, **v} for k, v in items[start:start + limit]], "page": page, "limit": limit, "total": len(items)}

@app.get("/v1/availability")
def availability(room_id: str, start_date: date, end_date: date):
    if start_date >= end_date:
        raise HTTPException(400, "start_date must be before end_date")
    if room_id not in rooms:
        raise HTTPException(404, "room not found")
    occupied = any(b["room_id"] == room_id and b["status"] == "confirmed" and start_date < b["end_date"] and end_date > b["start_date"] for b in bookings.values())
    return {"room_id": room_id, "available": not occupied}

@app.post("/v1/bookings", status_code=201)
def create_booking(payload: BookingRequest, authorization: Optional[str] = Header(None), idempotency_key: Optional[str] = Header(None)):
    if authorization != "Bearer user-a":
        raise HTTPException(401, "unauthorized")
    if payload.start_date >= payload.end_date:
        raise HTTPException(400, "start_date must be before end_date")
    room = rooms.get(payload.room_id)
    if room is None:
        raise HTTPException(404, "room not found")
    if payload.guests > room["capacity"]:
        raise HTTPException(400, "guest count exceeds room capacity")
    if idempotency_key and idempotency_key in idempotency:
        previous_payload, booking_id = idempotency[idempotency_key]
        if previous_payload != payload.model_dump():
            raise HTTPException(409, "idempotency key reused with different payload")
        return bookings[booking_id]
    overlap = any(b["room_id"] == payload.room_id and b["status"] == "confirmed" and payload.start_date < b["end_date"] and payload.end_date > b["start_date"] for b in bookings.values())
    if overlap:
        raise HTTPException(409, "room unavailable for requested dates")
    booking_id = f"booking-{len(bookings) + 1}"
    record = {"id": booking_id, "room_id": payload.room_id, "start_date": payload.start_date.isoformat(), "end_date": payload.end_date.isoformat(), "guests": payload.guests, "guest": payload.guest.model_dump(), "status": "confirmed", "owner": "user-a"}
    bookings[booking_id] = record
    if idempotency_key:
        idempotency[idempotency_key] = (payload.model_dump(), booking_id)
    return record

@app.get("/v1/bookings/{booking_id}")
def get_booking(booking_id: str, authorization: Optional[str] = Header(None)):
    if authorization not in ("Bearer user-a", "Bearer user-b"):
        raise HTTPException(401, "unauthorized")
    record = bookings.get(booking_id)
    if not record:
        raise HTTPException(404, "booking not found")
    if record["owner"] != authorization.removeprefix("Bearer "):
        raise HTTPException(404, "booking not found")
    return record

@app.delete("/v1/bookings/{booking_id}")
def cancel_booking(booking_id: str, authorization: Optional[str] = Header(None)):
    if authorization != "Bearer user-a":
        raise HTTPException(401, "unauthorized")
    record = bookings.get(booking_id)
    if not record:
        raise HTTPException(404, "booking not found")
    if record["status"] == "cancelled":
        return record
    record["status"] = "cancelled"
    return record
