# Incident retrospective — triage quality regression

> Synthetic incident exercise. No production outage occurred.

## Event

After a runbook update, a triage model starts classifying database-pool saturation as a generic performance issue and omits the specific pool-acquisition diagnostic.

## Impact (assumed for the exercise)

Support engineers spend extra time correcting the triage note. No automated action or customer message is sent because the product is read-only.

## Timeline (simulated)

- 09:10 — Support reviewer notices repeated low-specificity classifications in a reviewed sample.
- 09:20 — Team pauses expansion of the evaluation set and records affected cases.
- 09:35 — Engineer compares runbook keywords and retrieval traces.
- 10:00 — Retrieval set is updated to include connection-pool and acquisition-timeout terminology.
- 10:30 — Offline tests and live regression sample are rerun.
- 11:00 — Support reviewer rechecks the corrected outputs before resuming pilot evaluation.

## Root cause

The keyword retrieval layer did not adequately cover terms used by support engineers. The issue was in retrieval coverage, not in database runtime health.

## Corrective actions

1. Add vocabulary variants and an explicit retrieval recall test.
2. Track required-evidence recall separately from severity/category accuracy.
3. Keep a no-match path that escalates instead of using an unrelated article.
4. Review knowledge-base changes as code and preserve source identifiers.
5. Add a periodic review owner for runbook freshness.

## Learning

A valid JSON schema is not equivalent to a grounded diagnosis. Retrieval coverage, evidence validation and human review are separate controls and must be measured independently.
