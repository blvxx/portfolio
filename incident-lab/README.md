# Incident Investigation Lab — Payment Webhook Failure

> **Portfolio case | Simulated incident | Application Support / Technical Support / Integration Support**

## Incident summary
A fictional payment provider reports successful payments, but some storefront orders remain in \`pending_payment\`.

- **Severity:** SEV-2 (simulation)
- **Component:** Webhook handler
- **Impact:** Paid orders may not be confirmed in the storefront
- **Root cause:** Webhook signature configuration points to an outdated secret
- **Recovery:** Correct configuration, validate a test event, replay verified events safely, reconcile state

## Investigation workflow
1. [Incident ticket](docs/incident-ticket.md)
2. [Evidence logs](evidence/application.log) — includes signature errors, timeouts, downstream 5xx, duplicates, and delayed events
3. [Diagnostic SQL](sql/diagnostics.sql) — reconciliation, duplicate detection, and state mismatch checks
4. [API examples](api/webhook-examples.md)
5. [RCA](docs/rca.md)
6. [Incident recovery runbook](docs/recovery-runbook.md)
7. [Reconciliation runbook](docs/reconciliation-runbook.md)
8. [SQL reconciliation report](docs/sql-reconciliation-report.md) — sample findings from synthetic data
9. [Investigation findings](docs/investigation-findings.md)
10. [Python log analyzer](scripts/analyze_incident.py) — classify patterns and recommend triage checks
11. [Automated reconciliation](scripts/reconcile_payments.py) — compare order/payment exports and produce CSV + HTML findings
12. [Reconciliation utility documentation](docs/automated-reconciliation.md

## Sample dataset
CSV files in \`data/\` contain fictional order/payment records with deliberately injected state mismatches and a repeated provider payment ID. These are used for SQL investigation examples, not real customer or financial data.

## Run and test
From the repository root:

\`\`\`bash
python incident-lab/scripts/analyze_incident.py
python incident-lab/scripts/reconcile_payments.py  # CSV + HTML reports
python -m unittest discover -s incident-lab/scripts -v
\`\`\`

Python 3.10+, standard library only. The analyzer classifies signature/authentication failures, webhook timeouts, downstream HTTP 5xx, duplicate deliveries, and delayed events. CI is configured; the run status has not been independently verified here.

## Skills demonstrated
- Incident triage and impact assessment
- HTTP/API and webhook troubleshooting
- Log analysis and pattern classification
- SQL reconciliation and duplicate detection
- Integration diagnostics and idempotency
- Root Cause Analysis and recovery verification
- Runbook writing and operational communication

All records, timestamps, and incident details are fictional.
