# Payment/order reconciliation runbook

## Purpose
Safely investigate order/payment state mismatches during webhook incidents.

## Before changing data
- Confirm incident window and affected order IDs.
- Verify payment status in provider dashboard/API using provider payment ID.
- Confirm webhook signature validation and delivery history.
- Review duplicate event/payment identifiers.
- Export or snapshot current records for audit.

## Diagnosis
- Find successful payments whose order remains `pending_payment`.
- Find pending orders without successful payment records.
- Find multiple successful payment rows per order.
- Find provider payment IDs repeated across rows or orders.

## Recovery
1. Correct the underlying webhook configuration/secret reference first.
2. Verify a test webhook returns success and causes the expected state transition.
3. Reconcile candidate orders against the provider, not only local DB state.
4. Replay only confirmed events with idempotency safeguards.
5. Avoid direct status updates unless the approved recovery process explicitly allows them.
6. Monitor delivery, retries, queue lag, and downstream errors.

## Validation
- Target incident orders have consistent provider/payment/order states.
- No unintended duplicate payment or fulfillment transitions.
- Replay/reconciliation counts match incident scope.
- Keep a record of affected IDs, action, operator, and timestamps.

## Escalation
Escalate if provider status cannot be verified, duplicate payment IDs map to different orders, or recovery risks double-charge/double-fulfillment.

All data and scenario details in this lab are fictional.
