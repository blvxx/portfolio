# Product brief — Northstar Support Triage MVP

> Fictional business case for portfolio practice. Not a real client brief.

## Problem

Support specialists receive free-form incident descriptions. They manually identify affected service, severity, relevant runbook and first response. Queue handling is inconsistent, and notes often omit evidence or next diagnostic steps.

## Outcome sought

Reduce the time required to prepare a first-pass triage note while preserving engineer control over decisions and customer communication.

## MVP scope

- Accept a synthetic incident report from a support engineer.
- Retrieve relevant, approved runbook snippets.
- Produce a structured severity/category summary, hypotheses, read-only checks and draft response.
- Cite runbook source IDs and escalate when evidence is weak or severity is critical.
- Record non-sensitive operational metadata only.

## Out of scope

- Autonomous service restarts, deployment, credential rotation or configuration updates.
- Automatic email/customer replies or ticket closure.
- Production infrastructure access.
- Training or fine-tuning on customer tickets.
- Promise of automatic root-cause identification.

## Business and delivery constraints

| Constraint | Decision |
|---|---|
| Small initial delivery budget | Keep MVP to one triage path and a bounded local knowledge base |
| Support must trust recommendations | Require evidence IDs and confidence-based escalation |
| Customer data risk | Use synthetic examples; exclude credentials and personal data from logs |
| Operational risk | Read-only diagnostics only; human approval for changes |
| API spend uncertainty | Keep model name/key configurable and make live evaluation opt-in |
| No existing single source of truth | Version runbook records and expose stable evidence IDs |
| Release needs rollback path | Keep feature separately deployable and avoid modifying the existing lead bot |

## Success measures for a pilot (targets, not measured outcomes)

- At least 90% of triage outputs reference one or more retrieved runbook IDs.
- Zero state-changing commands appear in the generated diagnostic checklist after guardrail validation.
- At least 80% severity/category agreement on a reviewed 50-case evaluation set.
- Human support lead approves the draft before it is sent.
- API spend, p95 latency and refusal/error rates are tracked before any pilot expands.

## Main risks

- Incorrect severity may delay escalation.
- Runbook content can be stale or incomplete.
- Prompt injection may appear inside user-supplied incident text.
- Unsupported citations can create false confidence.
- LLM latency/cost may exceed the operational value.
- Sensitive content could be sent to an external model if intake rules are weak.

## Decision

Proceed with a synthetic, read-only MVP and require a human reviewer. Do not connect it to a real ticketing system until privacy, retention, model-provider settings, evaluation quality and escalation ownership are approved.
