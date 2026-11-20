# Root Cause Analysis (RCA) — INC-2026-014

## Root cause
The webhook handler loaded a signing-secret reference pointing to a previous secret version. The provider signed events with the active secret, so signature validation failed and the handler returned HTTP 401. Because the event was rejected before payment/order state processing, the orders remained `pending_payment`.

## Evidence
- Repeated `signature_validation_failed` log entries with `reason=secret_mismatch`.
- Provider-side payment status in the simulated evidence is `succeeded`.
- Database reconciliation shows order/payment state mismatch.
- Configuration review identifies a stale secret reference.
- Controlled event succeeds after correcting the reference.

## Contributing factors
- Secret rotation/config reference was not validated end-to-end.
- Alerting identified elevated webhook 4xx, but business-state reconciliation was also needed to understand customer impact.
- No automated canary webhook check after configuration change (in the simulated environment).

## Five Whys
1. **Why** did orders remain pending? The payment webhook was not processed.
2. **Why** was it not processed? The handler rejected the request with 401.
3. **Why** did signature validation fail? The receiver used the wrong secret version.
4. **Why** was the wrong version loaded? The configuration reference was stale.
5. **Why** was it not detected earlier? The rotation procedure lacked a post-change delivery verification/canary.

## Corrective actions
- **Immediate:** Correct the secret reference using the approved secret-management process.
- **Validation:** Send a provider test event and verify a successful response and state transition.
- **Recovery:** Reconcile affected orders/payments; replay only failed events with idempotency safeguards.
- **Monitoring:** Alert on webhook 401 rate and on paid-payment/pending-order mismatches.
- **Prevention:** Add a canary event after secret rotation and document ownership/version verification.

## Verification
The simulated evidence records a test event accepted at 09:55 UTC and reconciliation completed at 10:04 UTC for 18 affected orders, with zero duplicate transitions.

## What I would communicate
Payment provider records indicate the affected payments succeeded, but the application did not process the confirmation event. We corrected the webhook configuration, verified delivery with a test event, and reconciled affected records. We are monitoring webhook delivery and order/payment consistency.

## Lessons learned
A successful payment-provider status is not enough to confirm the customer journey. Support investigations should correlate provider events, application logs, webhook delivery status, and database state.
