# Incident Operations Toolkit

A unified command-line entry point for the synthetic Incident Investigation Lab.

## Run all diagnostics
From the repository root:

```bash
python incident-lab/scripts/incident_ops.py all
```

This runs log pattern analysis, order/payment reconciliation, then writes combined JSON and HTML summaries.

## Individual commands

```bash
python incident-lab/scripts/incident_ops.py analyze-logs
python incident-lab/scripts/incident_ops.py reconcile
python incident-lab/scripts/incident_ops.py summary
```

## Outputs
- `incident-lab/reports/reconciliation_findings.csv`
- `incident-lab/reports/reconciliation_report.html`
- `incident-lab/reports/incident_summary.json`
- `incident-lab/reports/incident_summary.html`

## Severity heuristic
The combined summary includes a triage-only impact tier: HIGH priority or at least three affected orders -> SEV-2; findings/affected orders -> SEV-3; clean inputs -> SEV-4. This is a portfolio heuristic, not a production incident policy. Validate severity using customer impact, duration, service availability, and actual incident procedures.

All inputs and findings are synthetic. The toolkit is read-only and does not trigger payment changes, refunds, replays, or remediation.
