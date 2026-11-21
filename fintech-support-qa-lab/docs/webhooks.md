# Webhook processing and support checks

## Contract

Endpoint: `POST /webhooks/payment-status`

The sender provides a JSON body with:
- `event_id` — unique event identifier (3–128 characters)
- `payment_id` — internal payment identifier
- `status` — `paid` or `failed` (the API schema also accepts enum values, but state-transition rules reject unsupported transitions)

The `X-Signature` header contains an HMAC-SHA256 digest of the exact raw request body. The demo accepts either a plain hexadecimal digest or a `sha256=` prefixed digest. Configure the shared secret with `WEBHOOK_SECRET`.

Example signature generation:

```python
import hashlib
import hmac

signature = hmac.new(
    b"replace-with-shared-secret",
    raw_request_body,
    hashlib.sha256,
).hexdigest()
```

## Idempotency behavior

- First delivery: validate signature and payload, apply the payment transition and store the event ID + payload hash in one database transaction.
- Exact retry: return HTTP 200 with `duplicate: true`; do not apply the transition again.
- Same event ID with a different payload: return HTTP 409.
- Unknown payment: return HTTP 404.
- Invalid signature: return HTTP 401.
- Unsupported payment transition: return HTTP 409.

The unique database constraint on `event_id` protects against concurrent duplicate deliveries. The payload hash prevents reuse of an event ID for different data.

## Troubleshooting checklist

1. Confirm the webhook endpoint is reachable and returns a 2xx response.
2. Compare the sender's event ID with the stored event record.
3. Verify that the sender signs the exact raw bytes, not re-serialized JSON.
4. Confirm both systems use the same secret and SHA-256 HMAC algorithm.
5. Check whether a 409 indicates an invalid state transition or event-ID conflict.
6. Check payment state after processing; retries must not cause a second state change.

## Security note

This is an educational implementation. Production systems should also define timestamp/replay windows, key rotation, payload size limits, structured audit logs, retry policy and monitoring. Never log the shared secret or request authorization data.
