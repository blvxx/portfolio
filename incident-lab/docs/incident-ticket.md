# Incident Ticket — INC-2026-014

## Summary
Customers report that checkout displays no confirmation after payment. Internal review shows payment provider events marked successful while Shop API orders remain in `pending_payment`.

## Severity and status
- Severity: SEV-2 (simulation)
- Status: Resolved in simulation
- Service: Checkout / Payments
- Incident window: 2026-11-20 09:12–10:04 UTC
- Detection: Support ticket + monitoring alert for webhook 4xx rate

## Customer impact
- 18 orders were identified as stuck in `pending_payment` during the incident window.
- Payment provider records indicate successful charges for the affected orders.
- The storefront did not show the expected paid/confirmed state.
- No evidence in this simulated dataset of duplicate charges.

## Symptoms
- Webhook endpoint returns HTTP 401.
- Signature validation errors appear in application logs.
- Payment provider reports successful payment events.
- Order status does not transition to `paid`.

## Initial hypotheses
1. Webhook signing secret mismatch or wrong secret loaded by the receiver.
2. Incorrect webhook endpoint configuration at provider.
3. Recent deployment introduced a validation regression.
4. Payload format changed unexpectedly.
5. Clock skew or canonicalization mismatch caused signature verification failure.

## Investigation plan
1. Confirm scope using alert and event timestamps.
2. Inspect webhook request metadata and application errors (do not log secrets).
3. Verify endpoint configuration and secret version without exposing secret values.
4. Compare payment-provider event status with database payment/order records.
5. Identify the failure point and confirm recovery with a controlled event.
6. Replay only eligible events after verifying idempotency safeguards.

## Timeline (UTC)
| Time | Event |
|---|---|
| 09:12 | First failed webhook in evidence |
| 09:15 | Alert threshold exceeded for webhook 401 responses |
| 09:21 | Support reports checkout confirmation missing |
| 09:28 | Investigation confirms successful provider payments |
| 09:36 | Signature validation failure isolated |
| 09:47 | Incorrect secret reference identified in simulated configuration |
| 09:55 | Configuration corrected; controlled test webhook accepted |
| 10:04 | Backlog reconciled; incident closed in simulation |

## Communication
Customer-facing update: Payment may have been completed successfully even if the order confirmation is missing. Avoid retrying payment until order/payment status has been checked.

## Closure criteria
- Webhook endpoint accepts a valid signed event.
- Invalid signatures remain rejected.
- Reconciliation identifies paid orders without matching paid order state.
- Recovery is idempotent and does not create duplicate payment/order transitions.
- Monitoring shows webhook failures back below alert threshold.
