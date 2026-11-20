# Incident Investigation Lab — Payment Webhook Failure

> **Portfolio case | Simulated production incident | Application Support / Technical Support / Integration Support**

## Incident summary

A simulated e-commerce system receives successful payment events from an external payment provider, but some orders remain in `pending_payment`. The checkout flow does not update the order state after payment.

- **Severity:** SEV-2 (simulation)
- **Affected component:** Payment webhook handler
- **Customer impact:** Paid orders are not confirmed in the storefront
- **Primary symptom:** Webhook requests return HTTP 401
- **Root cause:** The receiver validates the webhook signature using the wrong secret/configuration value
- **Resolution:** Correct the secret reference, replay safely, and verify order/payment consistency

This repository demonstrates a structured incident investigation—not a claim of a real production incident.

## Investigation workflow

1. [Incident ticket](docs/incident-ticket.md) — symptoms, impact, scope, initial hypotheses
2. [Evidence and logs](evidence/application.log) — timestamped application and webhook events
3. [Diagnostic SQL](sql/diagnostics.sql) — checks for stuck orders, payments, duplicates, and mismatches
4. [API examples](api/webhook-examples.md) — request/response and validation scenarios
5. [Root cause analysis](docs/rca.md) — cause, contributing factors, corrective and preventive actions
6. [Recovery runbook](docs/recovery-runbook.md) — safe operational steps
7. [Log analysis script](scripts/analyze_incident.py) — summarizes error patterns from the supplied log
8. [Investigation findings](docs/investigation-findings.md) — evidence summary and recommended operational controls
9. [Recovery runbook](docs/recovery-runbook.md) — safe operational steps

## Run and test

From the repository root:

```bash
python incident-lab/scripts/analyze_incident.py
python -m unittest discover -s incident-lab/scripts -v
```

The analyzer uses only the Python standard library. Unit tests cover successful parsing, webhook failure/success counts, empty logs, malformed lines, and missing files. GitHub Actions runs the analyzer and tests on pushes and pull requests affecting this project.

## Architecture (simplified)

```text
Customer -> Shop API -> Order DB
                    ^
Payment Provider -- webhook --> Webhook Handler
                                  |
                                  +-- validate signature
                                  +-- update payment record
                                  +-- transition order state
```

## Key evidence

- Payment provider reports successful payment.
- Webhook delivery attempts return `401`.
- The handler logs signature validation failures.
- Orders are still `pending_payment` while payment records are `succeeded`.

## How to reproduce the log analysis

Requires Python 3.10+; no third-party dependencies.

```bash
python scripts/analyze_incident.py evidence/application.log
```

## SQL

The SQL file uses PostgreSQL syntax and assumes illustrative tables:

- `orders(id, created_at, status, total_amount, customer_id)`
- `payments(id, order_id, provider, provider_payment_id, status, paid_at)`
- `webhook_events(id, provider_event_id, event_type, received_at, processing_status, error_message)`

The schema is intentionally illustrative. No live database is required.

## Skills demonstrated

- Incident triage and impact assessment
- HTTP/API troubleshooting
- Log analysis and correlation
- SQL-based data validation
- Webhook/integration troubleshooting
- Root Cause Analysis (RCA)
- Recovery planning and verification
- Clear incident documentation

## Disclaimer

All names, timestamps, records, logs, and incident details are fictional and generated for this portfolio exercise.
