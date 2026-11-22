# Engineering roadmap

## Guiding rule

Items marked Current are supported by the code or repository configuration. Items marked Planned are not implemented yet. A roadmap entry is not evidence that a feature exists.

## M0 — Operational safety

Status: Planned

- [ ] Verify whether the live host provides persistent storage for the SQLite database.
- [ ] Exercise backup and restore against a disposable database copy.
- [ ] Define data retention and deletion behaviour.
- [ ] Add rate limiting and request-size limits.
- [x] Add handler-level tests for enquiry submission, policy rejection, optional admin notification and missing sender. (PR #16)
- [x] Enforce private-chat-only access to the admin lead listing and test unauthorized/group access (PR #20).
- [x] Add handler-level tests for consent transitions, stale consent callbacks, invalid service callbacks and cancellation (PR #25).
- [ ] Define what is and is not safe to log.

Exit criteria:
- A documented restore exercise passes on a test copy.
- No real customer data is accepted while host persistence remains unverified.
- Critical authorization and user-flow tests run in CI.

## M1 — Application boundaries and testability

Status: Planned

- [x] Move enquiry submission policy into a framework-independent application service (PR #15).
- [x] Introduce a typed CreateEnquiry command for the application use case (PR #15).
- [x] Keep aiogram message and callback types inside the Telegram adapter for enquiry submission.
- [x] Introduce an EnquiryRepository protocol and focused application service tests (PR #15).
- [ ] Add structured error handling and correlation identifiers.
- [ ] Add static analysis and formatting checks to CI.

Exit criteria:
- Enquiry submission policy can be tested without a Telegram network connection.
- Adapter tests cover the main user flow (still planned).
- CI runs unit tests, lint and type checks.

## M2 — Durable workflows

Status: Planned; conditional on requirements

- [x] Add a transactional outbox for administrator notifications (PR #17).
- [x] Add bounded exponential retry, expired-lease recovery, unique event keys and per-claim lease fencing (PR #17).
- [x] Introduce forward-only SQLite schema migrations tracked by PRAGMA user_version (PR #18).
- [x] Make Telegram enquiry submission idempotent by chat/message identity, including concurrent replay handling (PR #23).
- [ ] Evaluate PostgreSQL for multi-instance or higher-concurrency operation.
- [ ] Evaluate Redis if FSM state must be shared across replicas.
- [x] Add notification delivery states: pending, processing, delivered and dead. (PR #17)

Exit criteria:
- A failed notification is retried with bounded backoff; exhausted events are visible for operator review.
- Lead and outbox event are committed atomically.
- Duplicate enqueue for the same lead-created event is prevented by a unique constraint.
- Replayed Telegram message submissions reuse the existing lead ID instead of creating another lead or outbox event.
- Remote delivery is explicitly at-least-once; exactly-once delivery is not claimed.
- Database schema changes are versioned and repeatable; fresh install, existing version-1 upgrade, idempotent startup and future-version rejection are tested.
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
- Existing tests cover database persistence, ordering, limits, input validation, application-service rules, selected Telegram handler orchestration, FSM transition/cancellation and admin authorization cases, outbox atomicity, lease claims, retries, dead-letter transition, dispatcher delivery, schema upgrades and idempotent Telegram message replays. They do not yet cover the complete Telegram conversation flow or real Bot API delivery.
