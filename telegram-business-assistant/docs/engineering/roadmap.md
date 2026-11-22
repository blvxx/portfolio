# Engineering roadmap

## Guiding rule

Items marked Current are supported by the code or repository configuration. Items marked Planned are not implemented yet. A roadmap entry is not evidence that a feature exists.

## M0 — Operational safety

Status: Planned

- [ ] Verify whether the live host provides persistent storage for the SQLite database.
- [ ] Exercise backup and restore against a disposable database copy.
- [ ] Define data retention and deletion behaviour.
- [ ] Add rate limiting and request-size limits.
- [ ] Add handler-level tests for consent, cancellation, invalid callbacks and admin authorization.
- [ ] Define what is and is not safe to log.

Exit criteria:
- A documented restore exercise passes on a test copy.
- No real customer data is accepted while host persistence remains unverified.
- Critical authorization and user-flow tests run in CI.

## M1 — Application boundaries and testability

Status: Planned

- [ ] Move enquiry use cases out of Telegram handlers into an application/service layer.
- [ ] Introduce typed request/result objects for application use cases.
- [ ] Keep aiogram message and callback types inside the Telegram adapter.
- [ ] Add repository interfaces and focused persistence tests.
- [ ] Add structured error handling and correlation identifiers.
- [ ] Add static analysis and formatting checks to CI.

Exit criteria:
- Business rules can be tested without a Telegram network connection.
- Adapter tests cover the main user flow.
- CI runs unit tests, lint and type checks.

## M2 — Durable workflows

Status: Planned; conditional on requirements

- [ ] Add a transactional outbox for administrator notifications.
- [ ] Add retry/backoff and idempotency rules.
- [ ] Introduce database migrations.
- [ ] Evaluate PostgreSQL for multi-instance or higher-concurrency operation.
- [ ] Evaluate Redis if FSM state must be shared across replicas.
- [ ] Add an explicit enquiry lifecycle and notification delivery state.

Exit criteria:
- A failed notification is recoverable without creating duplicate enquiries.
- Database schema changes are versioned and repeatable.
- Migration and rollback are tested using non-production data.

## M3 — AI workflow extension

Status: Planned; not part of the current Telegram MVP

- [ ] Add an LLM provider abstraction with timeouts and budgets.
- [ ] Add schema-constrained classification and extraction.
- [ ] Add deterministic evaluation datasets and versioned prompts.
- [ ] Measure task accuracy, precision/recall where appropriate, latency, cost and failure rate.
- [ ] Add allowlisted tools and explicit human approval for side effects.
- [ ] Add prompt-injection and data-boundary tests.
- [ ] Compare a deterministic rules-based baseline with the LLM solution.

Exit criteria:
- The LLM path improves a measured business metric over a deterministic baseline.
- Model output cannot bypass authorization or directly execute arbitrary side effects.
- Evaluation results are reproducible for a pinned model/prompt configuration.

## M4 — Operability and release discipline

Status: Planned

- [ ] Add structured logs with sensitive-field redaction.
- [ ] Add metrics and actionable alerts.
- [ ] Define service-level indicators and targets only after a baseline is measured.
- [ ] Add release notes and version tags.
- [ ] Add dependency review and vulnerability scanning.
- [ ] Run a failure/recovery exercise and record findings.

Exit criteria:
- An operator can identify common failure modes from logs and metrics.
- A release can be rolled back using documented steps.
- Recovery exercises have recorded evidence.

## Current evidence

- Live Telegram MVP: https://t.me/blvlxxbot
- Source: https://github.com/blvxx/portfolio/tree/main/telegram-business-assistant
- Existing tests cover database persistence, ordering, limits and input validation. They do not yet cover the complete Telegram conversation flow.
