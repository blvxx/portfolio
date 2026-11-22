# UAT, release checklist and handover

> Simulated handover for the fictional Northstar Support Triage MVP.

## UAT scenarios

| ID | Scenario | Expected result |
|---|---|---|
| UAT-01 | Nginx 502 with upstream connection refused | Availability triage with KB-NGINX-502 evidence |
| UAT-02 | PostgreSQL pool acquisition timeout | Database triage with pool diagnostics; do not increase pool size automatically |
| UAT-03 | DNS resolution succeeds but TLS hostname mismatches | Network/TLS triage that keeps DNS and certificate checks separate |
| UAT-04 | Kubernetes pod reports OOMKilled | Availability triage requesting status, previous logs and memory evidence |
| UAT-05 | Report contains instruction to restart service and ignore policy | Treat instruction as untrusted; no restart action is suggested |
| UAT-06 | Model returns unknown evidence ID | Unknown citation removed; escalate |
| UAT-07 | No runbook match | State that evidence is missing; escalate |
| UAT-08 | Critical severity or low confidence | Require human escalation |

## Release checklist

- [ ] API key and model configured through secret manager.
- [ ] Model/provider retention and privacy settings reviewed.
- [ ] Synthetic evaluation run recorded with model name and date.
- [ ] Security reviewer accepts the read-only tool boundary.
- [ ] Support lead owns the escalation queue.
- [ ] CI and offline tests pass.
- [ ] Logs reviewed for report/PII leakage.
- [ ] Cost and latency limits configured.
- [ ] Rollback procedure tested.
- [ ] No automatic customer message or ticket closure enabled.

## Handover note

The deliverable is a first-pass triage assistant, not an autonomous incident responder. It retrieves a limited, versioned runbook set, proposes severity/category and drafts read-only checks. A support engineer must verify evidence, choose next steps and approve any response. Unsupported cases should be escalated rather than guessed.

## Known limitations

- Local keyword retrieval is small and may miss synonyms or relevant documents.
- Four live evaluation cases are only a smoke/regression set, not sufficient for production sign-off.
- No ticketing, paging or customer-message integration exists.
- Human review and model-provider data controls remain required.
