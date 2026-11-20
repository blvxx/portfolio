# Investigation Findings — INC-2026-014

## Evidence-based conclusion

The supplied fictional logs show repeated webhook signature validation failures with HTTP 401 and reason `secret_mismatch`. The provider payment records shown in the evidence indicate successful payment, while reconciliation entries show corresponding orders still in `pending_payment`.

Configuration review identifies the receiver's secret reference as pointing to an older version. A controlled test event succeeds after the reference is corrected. The final reconciliation log records 18 affected orders and 18 processed events with zero duplicate transitions.

## Log sample summary

| Metric | Value |
|---|---:|
| Signature validation failures in sample | 3 |
| Controlled webhook processed successfully | 1 |
| Reconciled affected orders (reported by log) | 18 |
| Processed recovery events (reported by log) | 18 |
| Duplicate transitions (reported by log) | 0 |

**Important:** These are counts from this intentionally small, fictional log sample. The 18-order recovery result is a recorded simulation event, not independently represented by 18 individual records in the sample.

## Investigation reasoning

1. HTTP 401 and `secret_mismatch` point to signature verification rather than downstream business logic.
2. Successful provider payment status and pending order state establish a state mismatch.
3. A stale secret reference explains why events signed by the provider were rejected.
4. The successful controlled event after configuration correction validates the proposed fix in the scenario.
5. Reconciliation and idempotency checks are required before replaying events.

## Recommended operational controls

- Alert on webhook rejection rate and signature-validation error reasons.
- Alert on business-state mismatch: successful payment with non-paid order.
- Run a controlled webhook verification after secret rotation.
- Store and process provider event IDs idempotently.
- Replay only after reconciliation and review.
