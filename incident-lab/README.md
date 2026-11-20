# Incident Investigation Lab — Payment Webhook Failure

> **Portfolio case | Simulated incident | Application Support / Technical Support / Integration Support**

## Incident summary

A simulated e-commerce system receives successful payment events from an external payment provider, but some orders remain in \`pending_payment\`. The checkout flow does not update order state after payment.

- **Severity:** SEV-2 (simulation)
- **Affected component:** Payment webhook handler
- **Customer impact:** Paid orders are not confirmed in the storefront
- **Primary symptom:** Webhook requests return HTTP 401
- **Root cause:** The receiver validates signatures with an outdated secret reference
- **Resolution:** Correct the secret reference, replay safely, and verify order/payment consistency

This is a fictional portfolio investigation—not a claim of a real production incident.

## Investigation workflow

1. [Incident ticket](docs/incident-ticket.md) — symptoms, impact, scope, initial hypotheses
2. [Evidence and logs](evidence/application.log) — timestamped application/webhook events with secondary failure patterns
3. [Diagnostic SQL](sql/diagnostics.sql) — checks for stuck orders, payments, duplicates, and mismatches
4. [API examples](api/webhook-examples.md) — request/response and validation scenarios
5. [Root cause analysis](docs/rca.md) — cause, contributing factors, corrective and preventive actions
6. [Recovery runbook](docs/recovery-runbook.md) — safe operational steps
7. [Log analyzer](scripts/analyze_incident.py) — pattern classification, counters, and triage suggestions
8. [Investigation findings](docs/investigation-findings.md) — evidence summary and operational controls

## Run and test

From repository root:

\`\`\`bash
python incident-lab/scripts/analyze_incident.py
python -m unittest discover -s incident-lab/scripts -v
\`\`\`

Python 3.10+; standard library only. Tests cover pattern classification, parsing edge cases, empty logs, malformed lines, and missing files. GitHub Actions is configured for this folder; CI results have not been independently confirmed here.

## Diagnostic classifications

The analyzer recognizes signature/authentication failures, webhook timeouts, downstream HTTP 5xx, duplicate deliveries, and delayed delivery. It prints counters and suggested checks. The simulated evidence log includes examples of each, including a duplicate suppression event to illustrate idempotency.

## Architecture

\`\`\`
Customer -> Shop API -> Order DB
                    ^
Payment Provider -- webhook --> Webhook Handler
                                  +-- validate signature
                                  +-- update payment
                                  +-- transition order state
\`\`\`

## Skills demonstrated

- Incident triage and impact assessment
- HTTP/API and webhook troubleshooting
- Log parsing and pattern classification
- SQL-based data validation
- Integration diagnostics and idempotency
- Root Cause Analysis and recovery planning
- Clear incident documentation

All names, timestamps, records, logs, and incident details are fictional.
