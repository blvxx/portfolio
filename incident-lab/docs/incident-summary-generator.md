# Incident Summary Generator

Consolidates log pattern counts and payment reconciliation findings into JSON and a self-contained HTML incident summary.

## Usage
Run from repository root after generating reconciliation CSV:

```bash
python incident-lab/scripts/reconcile_payments.py
python incident-lab/scripts/incident_summary.py
```

Optional paths:

```bash
python incident-lab/scripts/incident_summary.py --logs path/app.log --findings path/findings.csv --json path/summary.json --html path/summary.html
```

The report combines priority, parsed log levels, known log patterns, reconciliation issue counts, affected order IDs, a root-cause hint, and suggested triage steps. It does not execute remediation. A root-cause hint is a hypothesis and must be validated with source systems.

All example data is fictional.
