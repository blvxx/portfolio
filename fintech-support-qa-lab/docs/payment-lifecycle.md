# Payment lifecycle

## States

- `pending` — payment was created and is awaiting a result.
- `paid` — payment completed successfully.
- `failed` — payment failed.

## Allowed transitions

```text
pending -> paid
pending -> failed
paid    -> (terminal)
failed  -> (terminal)
```

A request that attempts an unsupported transition returns HTTP 409 Conflict. A request for a missing payment returns HTTP 404 Not Found. Invalid request fields return HTTP 422 Unprocessable Entity.

## Support checks

When a customer reports that an order is not paid:

1. Ask for the order/customer reference; do not request card data or secrets.
2. Retrieve the payment using `GET /payments/{payment_id}` when an internal payment ID is known.
3. Compare the payment status and amount with the order record in the relevant system.
4. Check application logs around the event timestamp.
5. Record the observed state, request/correlation identifiers and next action.
6. Escalate discrepancies with evidence; never manually mark a real payment as paid.

All examples in this lab use synthetic data.
