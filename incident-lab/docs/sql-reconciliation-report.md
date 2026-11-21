# SQL Reconciliation — Sample Results

> Findings are calculated from the fictional CSV sample in `data/`. The dataset deliberately contains mismatches and duplicate records.

## Dataset
- Orders: 8
- Payment rows: 8
- Successful payment rows: 7
- Failed payment rows: 1

## Findings

| Finding | Sample result | Interpretation |
|---|---:|---|
| Paid payment rows where order is still pending | 5 rows across 4 orders | One order has a duplicate successful payment row |
| Unique affected order IDs | ORD-1042, ORD-1043, ORD-1047, ORD-1049 | Local order state does not reflect payment status |
| Failed payment rows | 1 (ORD-1045) | Do not mark this order paid |
| Repeated provider payment identifier | PROV-9007 (2 rows for ORD-1049) | Possible duplicate ingestion; verify against provider |

## Interpretation

The primary mismatch is payment status `succeeded` while order status remains `pending_payment`. The duplicate payment row for `PROV-9007` inflates row-level counts; distinguish payment rows from distinct orders when reporting impact.

Before remediation, verify each provider payment and use idempotent state transitions. Do not blindly replay events or create another payment/fulfillment action.

## Operator sequence

1. Query paid-but-pending rows and collect distinct affected order IDs.
2. Validate provider payment IDs and statuses externally.
3. Identify failed/no-payment orders separately.
4. Check duplicate provider IDs and event IDs.
5. Correct webhook configuration and confirm test delivery.
6. Replay only verified events with deduplication safeguards.
7. Re-run reconciliation and confirm the target incident scope is consistent.

Synthetic dataset; no real customers or payments.
