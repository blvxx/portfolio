# REST API Test Matrix

All cases are **Not Run**. Endpoint contracts are assumptions for a fictional service.

| ID | Method / endpoint | Scenario | Input | Expected |
|---|---|---|---|---|
| API-ROOM-01 | GET /rooms | Default listing | No query | 200; array and pagination metadata |
| API-ROOM-02 | GET /rooms | Page boundary | page=1, limit=1 | 200; one result; next/total consistent |
| API-ROOM-03 | GET /rooms | Invalid limit | limit=0 | 400; validation error |
| API-ROOM-04 | GET /rooms | Unsupported sort field | sort=unknown | 400 or documented fallback; no server error |
| API-AV-01 | GET /availability | Valid range | start < end | 200; availability payload |
| API-AV-02 | GET /availability | Reversed dates | start > end | 400; field-level error |
| API-AV-03 | GET /availability | Same-day/zero-length | start = end | 400 according to assumed contract |
| API-AV-04 | GET /availability | Missing room id | room_id omitted | 400 |
| API-AV-05 | GET /availability | Unknown room | room_id nonexistent | 404 or documented empty result |
| API-BOOK-01 | POST /bookings | Valid booking | Valid dates, room, guest | 201; booking ID and created state |
| API-BOOK-02 | POST /bookings | Missing guest name | guest omitted | 400; no booking created |
| API-BOOK-03 | POST /bookings | Invalid email | malformed email | 400; validation details |
| API-BOOK-04 | POST /bookings | Negative guest count | guests=-1 | 400 |
| API-BOOK-05 | POST /bookings | Guests exceed capacity | guests>room capacity | 409 or validation error |
| API-BOOK-06 | POST /bookings | Overlapping booking | Same room/date conflict | 409; no duplicate reservation |
| API-BOOK-07 | POST /bookings | Retry with idempotency key | Same request/key repeated | Same booking returned; no duplicate |
| API-BOOK-08 | POST /bookings | Retry with different payload/key | Same key, altered payload | 409 or documented conflict |
| API-BOOK-09 | POST /bookings | Missing auth | Token omitted | 401 |
| API-BOOK-10 | POST /bookings | Invalid auth | Malformed/expired token | 401 |
| API-GET-01 | GET /bookings/{id} | Own booking | Authorized owner | 200; only own data |
| API-GET-02 | GET /bookings/{id} | Other user's booking | Different user token | 403 or privacy-safe 404 |
| API-GET-03 | GET /bookings/{id} | Unknown ID | Nonexistent ID | 404 |
| API-CAN-01 | DELETE /bookings/{id} | Cancel active booking | Owner token | 200/204; state cancelled |
| API-CAN-02 | DELETE /bookings/{id} | Cancel twice | Already cancelled | Idempotent response or documented conflict |
| API-CAN-03 | DELETE /bookings/{id} | Cancel without auth | Token omitted | 401 |
| API-ERR-01 | Any endpoint | Error payload | Invalid input | Consistent JSON error schema; no stack trace |
