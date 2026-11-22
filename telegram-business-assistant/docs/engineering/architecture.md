# Architecture: Telegram Business Assistant

## Document status

This document separates implemented behaviour from proposed improvements. The project is an independently developed portfolio MVP with a live Telegram demo; it is not presented as a commercial client deployment.

## Product scope

The application collects structured service enquiries in a Telegram chat and makes them available to a configured administrator.

Current workflow:
1. A visitor starts the bot.
2. The bot explains the enquiry flow and asks for consent.
3. The visitor selects a service category.
4. The visitor provides a phone number, email address or Telegram contact.
5. The visitor describes the request.
6. The application writes the enquiry to SQLite.
7. The visitor receives a confirmation.
8. If an administrator chat is configured, the bot attempts to send a notification.

The application does not currently connect to a CRM, process payments or use an LLM.

## Current runtime architecture

Telegram Bot API
  -> aiogram Dispatcher (long polling)
  -> Telegram Router / Handlers
      -> consent and service selection
      -> contact and text validation
      -> administrator commands
  -> SQLite persistence adapter (aiosqlite)

Conversation state is held in aiogram MemoryStorage.

| Component | Responsibility | Current implementation |
|---|---|---|
| Entry point | Load settings, initialize dependencies and start polling | src/bot.py |
| Configuration | Read and validate environment settings | src/config.py |
| Telegram interface | Handle commands, callbacks and messages | src/handlers.py |
| Conversation state | Track the visitor's current step | aiogram MemoryStorage |
| Validation | Validate contact and request text | src/validation.py |
| Persistence | Initialize schema and store/read enquiries | src/database.py |
| UI controls | Build inline keyboards and service catalog | src/keyboards.py |

The current handler module coordinates Telegram interaction and calls the database adapter directly. A dedicated application/service layer is a planned refactoring, not a current capability.

## Data model

The current SQLite table stores:
- generated lead ID;
- Telegram user ID and optional username;
- customer display name;
- submitted contact;
- selected service;
- request description;
- UTC creation timestamp.

The schema is created during startup. The current repository does not include a versioned database migration framework.

## Runtime and deployment assumptions

- The bot uses Telegram long polling.
- The current deployment is a single background worker.
- Docker Compose uses one named volume for the SQLite data directory.
- The container runs as a non-root user, has a read-only root filesystem, drops Linux capabilities and enables no-new-privileges.
- Conversational FSM state is held in process memory and is lost on restart.
- The hosted Dada Cloud deployment has no verified persistent-volume guarantee. The README warns against collecting real customer enquiries until storage and backups are verified.

The current data store is suitable only for the documented single-instance MVP assumptions. SQLite must not be treated as shared multi-replica storage.

## Failure semantics

| Failure | Current behaviour | Engineering concern |
|---|---|---|
| Process restart | Unfinished FSM flow is lost | Visitor may need to restart |
| SQLite unavailable | Lead write fails; no durable fallback | User-facing error path and alerting need improvement |
| Admin notification fails | Lead remains stored; notification exception is logged | No retry queue or delivery state exists |
| Telegram API unavailable | Polling or message operations may fail | Recovery and operational visibility are limited |
| Host storage is ephemeral | SQLite file may be lost after replacement | Persistence must be verified before real data collection |

A successful database write and a successful administrator notification are separate outcomes. The current application does not implement an outbox or guaranteed notification delivery.

## Proposed target architecture (not implemented)

Telegram Adapter / HTTP API
  -> Application Services
      -> Enquiry use cases
      -> Consent and policy checks
      -> Notification orchestration
  -> Persistence Ports -> PostgreSQL (when requirements justify it)
  -> Integration Ports -> Telegram / CRM / n8n
  -> Durable outbox -> background worker
  -> Redis for shared FSM state, if multi-instance operation is required
  -> Observability: structured logs, metrics, traces and alert rules

A modular monolith is the preferred first target. Separate deployable microservices are not justified until independent scaling or ownership requirements exist.

## Design principles

- Prefer a simple modular monolith before distributed services.
- Keep Telegram-specific types out of core business rules.
- Make persistence and notification outcomes explicit.
- Use idempotency for retried external events.
- Keep personal data out of ordinary application logs.
- Treat LLM output as untrusted input if an AI capability is added.
- Require human approval for high-impact external actions.
- Record architectural decisions and revise them when requirements change.

## Open engineering questions

- What enquiry retention period is appropriate for the intended operator?
- Which persistent host/storage guarantee is available for the live demo?
- Is PostgreSQL required now, or only when requirements justify it?
- Does the operator need a retry workflow for administrator notifications?
- Which service-level objectives are meaningful for this application?
- What data should be visible to an administrator, and for how long?

These questions must be resolved before positioning the application as suitable for real customer data.
