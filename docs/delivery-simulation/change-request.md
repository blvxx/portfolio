# Change request CR-02 — request for automatic ticket closure

> Simulated change-control exercise. Fictional stakeholders and approval.

## Request

The fictional Support Operations Lead asks to add a feature that automatically closes low-severity tickets when the agent generates a customer response.

## Impact assessment

| Dimension | Assessment |
|---|---|
| User value | Could reduce manual queue work |
| Risk | High: incorrect classification or draft response could close a valid issue |
| Scope | Adds a ticketing integration and write permission |
| Security | Requires a privileged credential and audit controls |
| Test burden | Requires contract tests, duplicate-event handling, retry semantics and rollback |
| Delivery cost | Material increase relative to the read-only MVP |

## Decision

**Deferred from MVP.** No write-capable ticketing connector will be added in this release.

## Rationale

The MVP has not yet demonstrated reliable classification on a sufficiently reviewed data set. Automatic closure is difficult to reverse and creates material business risk. The current product brief specifically requires a human to approve messages and operational changes.

## Conditions for reconsideration

1. A reviewed evaluation set meets agreed quality thresholds.
2. Ticketing API access is scoped to draft creation rather than closure.
3. A human approval step and immutable audit record are implemented.
4. Duplicate/retry and rollback behaviour are tested.
5. Security/privacy review accepts the data flow.
6. Product Owner explicitly approves the scope and release trade-off.

## Stakeholder update draft

"We've assessed automatic closure as valuable but not safe for the first release. We'll keep triage and reply generation read-only, measure quality with a reviewed case set, and revisit ticket integration after the approval/audit controls are in place."
