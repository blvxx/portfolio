# Simulated pull-request review record

> Review comments below are fictional training artefacts. They are not feedback from actual teammates or maintainers.

## Pull request

Feature: retrieval-grounded support triage agent.

## Reviewer A — Support Operations (simulated)

**Comment:** "What happens if the model cites an article it never retrieved?"

**Response:** The application checks every evidence ID against the exact retrieved document set. Unknown IDs are removed, and the result is marked for escalation. Unit tests cover fabricated source IDs.

## Reviewer B — Security (simulated)

**Comment:** "The incident text can contain instructions that try to make the agent run commands or disclose credentials."

**Response:** The incident is passed as untrusted content, the system prompt restricts the task to runbook-grounded triage, the model has no external tools, and a post-generation guardrail removes state-changing recommendations. Tests cover prompt-injection-shaped input and suggestions such as restart/delete/deploy.

## Reviewer C — QA (simulated)

**Comment:** "A structured schema does not prove that the diagnosis is correct."

**Response:** Schema adherence is treated as an output contract, not a correctness guarantee. The project includes a live-model regression evaluator for severity/category agreement and required evidence recall. A reviewed case set and human approval remain mandatory.

## Review disposition

All three comments are accepted as release risks and reflected in implementation or explicit limitations. Since this exercise is self-authored, it does not claim an independent code review or real team collaboration.
