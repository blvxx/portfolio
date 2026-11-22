# Simulated API Defect Reports

All defects below are hypothetical examples, not observed or verified against a real API.

## API-BUG-01 — Overlapping reservation returns success
- **Severity:** Critical (proposed), **Priority:** P0
- **Endpoint:** POST /v1/bookings
- **Steps:** Create booking for room-101; submit another booking with overlapping dates.
- **Expected:** 409 Conflict; second booking not persisted.
- **Hypothetical actual:** 201 Created; overlapping booking persisted.
- **Risk:** Room double-booking.
- **Evidence:** Not available; hypothetical.

## API-BUG-02 — Booking details disclose another customer's data
- **Severity:** Critical (proposed), **Priority:** P0
- **Endpoint:** GET /v1/bookings/{id}
- **Steps:** Authenticate as user B; request booking ID belonging to user A.
- **Expected:** 403 or privacy-safe 404; no personal data returned.
- **Hypothetical actual:** 200 response includes guest name/email.
- **Risk:** Privacy breach.
- **Evidence:** Not available; hypothetical.

## API-BUG-03 — Invalid date range produces 500
- **Severity:** Major (proposed), **Priority:** P1
- **Endpoint:** GET /v1/availability
- **Steps:** Send start_date later than end_date.
- **Expected:** 400 with structured validation error.
- **Hypothetical actual:** 500 Internal Server Error.
- **Risk:** Client sees server failure for invalid input.
- **Evidence:** Not available; hypothetical.

## API-BUG-04 — Idempotency key is ignored
- **Severity:** Major (proposed), **Priority:** P1
- **Endpoint:** POST /v1/bookings
- **Steps:** Submit identical booking twice using same idempotency key.
- **Expected:** Same booking response or safe duplicate handling.
- **Hypothetical actual:** Two booking records created.
- **Risk:** Duplicate reservations and inconsistent billing.
- **Evidence:** Not available; hypothetical.
