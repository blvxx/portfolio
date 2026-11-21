# Demonstration Scenario — Payment Confirmation Incident

> Portfolio simulation. All orders, events, logs, timestamps, and findings are fictional.

## Scenario briefing

**INC-2026-014 · SEV-2 simulation · Checkout / payments**

Support receives a report: customers say the payment completed, but checkout never displays confirmation. Payment provider status is reported as successful, while orders remain in `pending_payment`.

### Interview-sized problem statement
"Investigate why successful payments are not reflected in order status, determine scope, identify the failure point, recommend safe recovery, and verify that recovery does not create duplicate state transitions."

## Walkthrough: what the engineer does

### 1. Establish scope and customer impact
- Review incident ticket and timeline.
- Identify affected component: webhook receiver / order state update.
- Confirm whether the symptom is isolated or widespread.
- Avoid asking customers to retry payment before checking provider/order status.

**Evidence:** [Incident ticket](incident-ticket.md), [application log](../evidence/application.log).

### 2. Inspect logs and find the pattern

Run from repository root:

```bash
python incident-lab/scripts/analyze_incident.py
python incident-lab/scripts/incident_ops.py analyze-logs
```

Look for recurring signature-validation failures (HTTP 401), timeout and downstream 5xx events. Correlate event IDs and timestamps rather than treating every line as a separate root cause.

**Interpretation:** signature failures are a strong lead, not sufficient proof by themselves.

### 3. Compare payment and order states

Review the diagnostic SQL:
- Successful payment with order still pending.
- Multiple successful payment rows for one order.
- Reused provider payment IDs.
- Pending orders without a successful payment record.

Run the synthetic reconciliation utility:

```bash
python incident-lab/scripts/reconcile_payments.py
```

Review `incident-lab/reports/reconciliation_findings.csv` and the HTML report. The utility is read-only and flags inconsistencies; it does not make financial changes.

### 4. Narrow down root cause

Working hypotheses:
1. Secret mismatch / stale secret reference.
2. Provider endpoint configuration mismatch.
3. Deployment regression.
4. Payload/signature canonicalization change.
5. Clock skew.

Use the available evidence to narrow the hypothesis. In this scenario, config review indicates the receiver uses a previous signing-secret reference. Do not reveal secret values in logs or tickets.

### 5. Propose safe recovery

1. Correct the secret reference through the approved secret-management process.
2. Send a controlled provider test event.
3. Verify the receiver accepts the signature and the order state transition succeeds.
4. Reconcile the affected set against authoritative provider records.
5. Replay only eligible events with idempotency/deduplication protections.
6. Monitor 4xx rate, queue lag, timeouts, and paid-vs-pending mismatch.

**Do not** blindly replay, refund, or manually mark orders paid without authoritative verification and approval.

### 6. Verify and close

Closure criteria:
- Valid test event accepted.
- Invalid signature still rejected.
- Affected orders reconciled with provider evidence.
- No duplicate transitions introduced.
- Monitoring returns to expected baseline.

The synthetic incident log records a successful controlled test and a reconciliation completion. These are simulated records, not live system results.

## One-command demo

From the repository root:

```bash
python incident-lab/scripts/incident_ops.py all
```

Expected artifacts:
- `incident-lab/reports/reconciliation_findings.csv`
- `incident-lab/reports/reconciliation_report.html`
- `incident-lab/reports/incident_summary.json`
- `incident-lab/reports/incident_summary.html`

Run the tests:

```bash
python -m unittest discover -s incident-lab/scripts -v
```

## 90-second interview explanation

"I built a synthetic incident investigation case around payment webhooks. The symptom was successful provider payments with orders stuck in pending. I started by establishing scope and correlating timestamps and event IDs in logs. Then I compared payment and order records using SQL and a Python reconciliation utility, which flags mismatches and duplicate identifiers. Evidence pointed to a webhook signature failure caused by a stale secret reference. I documented a safe recovery: validate configuration, send a controlled test event, reconcile against the provider, and replay only with idempotency checks. I also added a CLI to run the diagnostics and produce HTML/JSON reports. The dataset is synthetic, so I clearly distinguish simulated evidence from production experience."

## Interview questions to rehearse

- Why is HTTP 401 returned by the webhook?
- Why is payment provider success not the same as order status being paid?
- What evidence distinguishes the root cause from a hypothesis?
- Why is replay dangerous without idempotency?
- Which SQL query would you run first and why?
- What metrics/alerts would you monitor after recovery?
- What information should be included in an incident update?

## Honest portfolio framing

This is a **self-directed simulation**, not a real production incident or commercial project. It demonstrates troubleshooting workflow, log reading, SQL investigation, Python tooling, documentation, and operational judgment.
