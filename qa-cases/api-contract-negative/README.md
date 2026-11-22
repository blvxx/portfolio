# QA Case: REST API Contract & Negative Testing

> Fictional booking API. This is a designed test case pack, not testing performed against a live service.

## Scenario
A reservation API exposes rooms, availability and booking creation. QA focuses on input validation, status codes, data integrity, authorization boundaries and retry behavior.

## Scope
- `GET /rooms`: filtering and pagination
- `GET /availability`: date range and room id validation
- `POST /bookings`: required fields, date constraints, guests, conflict handling
- `GET /bookings/{id}`: existence and ownership
- `DELETE /bookings/{id}`: cancellation state

## Files
- [API test matrix](test-matrix.md)
- [Sample requests and responses](examples.md)
- [Simulated bug reports](bug-reports.md)

## Risk-based focus
P0: double-booking, unauthorized access to booking details, booking with invalid date ranges.
P1: incorrect validation/status code, pagination/filtering regressions.
P2: error payload consistency and response metadata.

## Assumptions
API base URL is `https://api.example.test/v1`; endpoints and payloads are invented for this exercise. No real service was contacted. All simulated defects are explicitly hypothetical.
