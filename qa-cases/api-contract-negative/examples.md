# Request / Response Examples (Proposed Contract)

Examples use a fictional endpoint and are not captured from a live service.

## Create booking — success
```http
POST /v1/bookings
Authorization: Bearer <token>
Idempotency-Key: 8d7f0c3e-qa-example
Content-Type: application/json
```
```json
{
  "room_id": "room-101",
  "start_date": "2027-03-12",
  "end_date": "2027-03-15",
  "guests": 2,
  "guest": {
    "name": "Test Guest",
    "email": "qa@example.test"
  }
}
```

Expected: `201 Created`, booking identifier, state `confirmed`, and date/room values matching request.

## Validation failure
Expected `400 Bad Request` for reversed dates. Error shape:
```json
{
  "error": {
    "code": "INVALID_DATE_RANGE",
    "message": "start_date must be before end_date",
    "field": "start_date"
  }
}
```

## Conflict
Expected `409 Conflict` for overlapping room reservations. No additional booking should be created.

## Authorization
A user requesting another user's booking should receive `403` or privacy-safe `404`; response must not expose guest contact details.
