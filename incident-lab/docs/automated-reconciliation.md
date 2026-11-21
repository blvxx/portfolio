# Automated Order/Payment Reconciliation

This script compares order and payment CSV exports and writes actionable findings.

## Checks
- Missing payment records
- Successful payment with an order not marked `paid`
- Failed and pending/processing payment records
- Multiple payment records linked to one order
- Repeated provider payment IDs

## Usage
From the repository root:

```bash
python incident-lab/scripts/reconcile_payments.py
python -m unittest discover -s incident-lab/scripts -p "test_reconcile_payments.py" -v
```

Optional custom files and output path:

```bash
python incident-lab/scripts/reconcile_payments.py --orders path/orders.csv --payments path/payments.csv --output path/report.csv
```

Output is a CSV with severity, issue type, order ID, payment IDs, details, and recommended next action. The tool is read-only: it never changes order/payment data, triggers refunds, or replays events.

All included records are fictional. Findings should be validated against the payment provider and system of record before taking action.
