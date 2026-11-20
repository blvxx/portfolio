# Webhook API Troubleshooting Examples

These examples are fictional. The endpoint and payload are placeholders; never include real secrets in commands, screenshots, logs, or repository history.

## Expected successful delivery

```http
POST /webhooks/payments HTTP/1.1
Host: shop.example.test
Content-Type: application/json
X-Provider-Event: payment.succeeded
X-Webhook-Signature: <signature-generated-with-test-secret>

{
  "event_id": "evt_test_88",
  "type": "payment.succeeded",
  "data": {
    "order_id": "ORD-TEST-1",
    "payment_id": "pay_test_1",
    "status": "succeeded"
  }
}
```

Expected: HTTP 200 or 204, event recorded as processed, order state transitions once to `paid`.

## Failure matrix

| Response | Possible meaning | Checks |
|---|---|---|
| 400 | Invalid body or missing required field | JSON structure, required fields, content type |
| 401 | Authentication/signature failure | Secret version, raw-body signing, header, rotation state |
| 403 | Authenticated but not authorized | Provider permissions, endpoint policy |
| 404 | Wrong endpoint or resource | URL, route, environment |
| 409 | Duplicate/conflicting transition | Idempotency key, event already processed |
| 429 | Rate limited | Retry policy, backoff, provider limits |
| 5xx | Handler or downstream failure | App logs, dependencies, DB connectivity |

## Diagnostic checklist for 401 signature failures

1. Confirm the webhook is reaching the expected environment and endpoint.
2. Check which secret version/config reference is loaded—never print the secret.
3. Confirm signature is calculated against the raw request body if provider requires it.
4. Confirm header name and signature algorithm match provider documentation.
5. Check key rotation timing and deployment/config cache.
6. Compare a provider-generated test event with local validation.
7. Keep invalid signatures rejected; do not bypass verification to restore service.

## Retry and idempotency

Webhook providers commonly retry failed deliveries. Recovery must be idempotent:
- Store provider event ID and reject or safely ignore duplicates.
- Use atomic state transitions.
- Reconcile payment and order records before replay.
- Do not trigger a second charge when replaying a notification.
