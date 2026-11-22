# Prioritised backlog

> Fictional backlog used to practice delivery planning. No real client tickets are represented.

## Prioritisation method

Use a lightweight impact / effort score: business risk reduction and user value are considered first, with effort and dependency as tie-breakers. Scores are relative planning inputs, not measured financial returns.

| ID | Priority | Story | Acceptance criteria | Effort |
|---|---|---|---|---|
| TRIAGE-01 | P0 | As a support engineer, I can submit a bounded incident report | Empty, too-short and over-limit reports are rejected; report length is capped; no credentials are requested | S |
| TRIAGE-02 | P0 | As a support engineer, I receive relevant runbook references | Each source has a stable ID; retrieval returns only known documents; no-match result is explicit | M |
| TRIAGE-03 | P0 | As a support lead, I receive a structured triage result | Severity/category/schema are valid; summary, hypotheses, checks and draft are present | M |
| TRIAGE-04 | P0 | As a security reviewer, I need untrusted input contained | Incident text is marked untrusted; prompt-injection instructions are ignored; model has no write tools | M |
| TRIAGE-05 | P0 | As a support lead, I need safe escalation | Unknown citations are removed; missing evidence/low confidence/critical severity escalates | S |
| TRIAGE-06 | P1 | As a QA reviewer, I need repeatable offline tests | Fake-provider tests cover valid result, missing evidence, invalid citation and state-changing recommendation | M |
| TRIAGE-07 | P1 | As a product owner, I need to compare model revisions | Live evaluation reports severity/category agreement and evidence recall over reviewed synthetic cases | M |
| TRIAGE-08 | P2 | As an operations owner, I need service insight | Record latency, token usage, spend and model errors without raw reports | M |
| TRIAGE-09 | P2 | As an administrator, I need controlled publication | Human approval gate exists before any customer message or ticket mutation | L |

## Sprint-1 commitment

Deliver TRIAGE-01 through TRIAGE-06 only. TRIAGE-07 is an opt-in evaluator, not a release gate. TRIAGE-08 and TRIAGE-09 remain out of the first iteration to avoid expanding the security surface.

## Definition of Done

- Acceptance criteria and negative paths are tested.
- Source IDs are verifiable and any ungrounded output escalates.
- No customer-facing or infrastructure action is executed.
- CI passes from a clean checkout.
- Setup, configuration, limitations and rollback are documented.
- No secrets or personal data appear in repository content or test logs.
