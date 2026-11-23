# Incident Investigation Lab — Payment Webhook Failure

> **Portfolio case | Simulated incident | Application Support / Technical Support / Integration Support**

## Incident summary

A fictional payment provider reports successful payments, but some storefront orders remain in `pending_payment`.

| Field | Detail |
|---|---|
| Severity | SEV-2 (simulation) |
| Component | Webhook handler / payment-order state synchronization |
| Impact | Paid orders may remain unconfirmed in the storefront |
| Root cause | Webhook signature configuration references an outdated secret |
| Recovery | Correct configuration, validate a test event, safely replay verified events and reconcile state |

All logs, timestamps, payments and orders in this lab are fictional. No production system or real customer/payment data is represented.

## Investigation path

This case follows a support investigation from initial report through diagnosis and recovery:

1. **[Incident ticket](docs/incident-ticket.md)** — initial report, scope and symptoms.
2. **[Evidence logs](evidence/application.log)** — signature failures, timeouts, downstream 5xx, duplicate and delayed events.
3. **[API examples](api/webhook-examples.md)** — webhook request/response behavior.
4. **[Diagnostic SQL](sql/diagnostics.sql)** — reconciliation, duplicate detection and state mismatch checks.
5. **[Investigation findings](docs/investigation-findings.md)** — evidence and timeline.
6. **[RCA](docs/rca.md)** — root cause, contributing factors and prevention.
7. **[Recovery runbook](docs/recovery-runbook.md)** — safe restoration steps.
8. **[Reconciliation runbook](docs/reconciliation-runbook.md)** — verification of payment/order consistency.
9. **[SQL reconciliation report](docs/sql-reconciliation-report.md)** — sample findings from synthetic data.

## Operations toolkit

The unified CLI combines the lab's diagnostics into a reproducible workflow.

Run from the repository root:

```bash
python incident-lab/scripts/incident_ops.py all
```

Individual commands:

```bash
python incident-lab/scripts/incident_ops.py analyze-logs
python incident-lab/scripts/incident_ops.py reconcile
python incident-lab/scripts/incident_ops.py summary
```

The toolkit includes:
- **Log analysis** — classify signatures, timeout, downstream failures, duplicates and delayed webhook patterns.
- **Payment reconciliation** — compare synthetic payment/order records and export CSV + HTML findings.
- **Incident summary** — combine diagnostics into machine-readable JSON and an HTML report.

See the [operations toolkit guide](docs/incident-operations-toolkit.md) for output paths and the severity heuristic.

## Additional utilities

- [Python log analyzer](scripts/analyze_incident.py) — pattern classification and suggested triage checks.
- [Automated reconciliation](scripts/reconcile_payments.py) — CSV and HTML findings.
- [Incident summary generator](scripts/incident_summary.py) — combined JSON and HTML.
- [Incident report template](docs/incident-report-template.md) — reusable incident documentation.

## Sample dataset

CSV files in `data/` contain fictional order/payment records with deliberately injected state mismatches and a repeated provider payment ID. These are used for SQL investigation and reconciliation examples—not real customer or financial data.

## Run and test

Python 3.10+; standard library only.

```bash
python incident-lab/scripts/analyze_incident.py
python incident-lab/scripts/reconcile_payments.py
python -m unittest discover -s incident-lab/scripts -v
```

The analyzer classifies signature/authentication failures, webhook timeouts, downstream HTTP 5xx, duplicate deliveries and delayed events. CI is configured; verify the latest Actions run for actual pass/fail evidence.

## Skills demonstrated

- Incident triage and impact assessment
- HTTP/API and webhook troubleshooting
- Log analysis and pattern classification
- SQL reconciliation and duplicate detection
- Integration diagnostics and idempotency
- Root Cause Analysis and recovery verification
- Runbook writing and operational communication
