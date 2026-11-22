# Telegram Business Assistant

A live Telegram bot MVP for small businesses to collect structured enquiries and route them to an administrator.

**Live demo:** [@blvlxxbot](https://t.me/blvlxxbot)

**Deployment validation:** the hosted bot's main enquiry flow was confirmed before the recent outbox and migration refactor. The current source in `main` passes CI, but the hosted instance has not yet been smoke-tested against these latest changes.

This portfolio project demonstrates a lead-capture workflow with consent, validation, SQLite persistence and an optional durable administrator-notification outbox.

## What it does

- Shows a clear entry menu and explains the available service scenarios.
- Collects explicit consent before asking for personal contact details.
- Lets a visitor choose the type of enquiry.
- Accepts a phone number, email address or Telegram shared contact.
- Validates the contact and request description.
- Stores each enquiry in SQLite with a UTC timestamp and a stable Telegram message idempotency key.
- Repeated processing of the same chat/message identity returns the existing enquiry instead of creating a duplicate.
- When ADMIN_CHAT_ID is configured, inserts a notification event in the same database transaction as the enquiry.
- Runs a background worker that claims notification events, sends them through Telegram and records delivery/retry state.
- Provides /my_id to display the numeric IDs needed for administrator setup.
- Provides a restricted /leads command for an administrator configured with ADMIN_USER_ID.
- Includes /cancel to stop an unfinished request.

## Stack

- Python 3.11+
- aiogram 3.x
- aiosqlite / SQLite
- pytest and pytest-asyncio
- GitHub Actions

## Architecture

    Telegram Update
          |
          v
    aiogram Router
          |
          v
    Enquiry Application Service
          |
          v
    SQLite transaction
      |             |
      v             v
    leads       notification_outbox
                      |
                      v
              Background worker
                      |
                      v
              Telegram notification

The bot keeps conversational state in aiogram MemoryStorage. Lead records and notification events are persisted in SQLite and survive process restarts only when the database file is placed on persistent storage. The schema is versioned with forward-only migrations and upgraded automatically on startup; take a verified backup before deploying a schema change. Telegram submissions use a unique key derived from chat ID and message ID, so a replay returns the original lead ID and does not add a second notification event. The outbox uses atomic event creation, exclusive claims, per-claim lease tokens, bounded exponential retry and a dead state after five failed attempts. Delivery is at-least-once, not exactly-once: a crash after Telegram accepts a message but before the local delivered marker commits can cause a duplicate. For a multi-instance production deployment, replace MemoryStorage with Redis and evaluate a shared database such as PostgreSQL.

## Run locally

1. Use Python 3.11 or newer.
2. Create a virtual environment and install dependencies:

       python -m venv .venv
       # Windows:
       .venv\\Scripts\\activate
       # macOS / Linux:
       source .venv/bin/activate
       pip install -r requirements-dev.txt

3. Copy .env.example to .env.
4. Create a Telegram bot with @BotFather and place its token in BOT_TOKEN.
5. Optionally set ADMIN_CHAT_ID and ADMIN_USER_ID.
6. Start the bot:

       python -m src.bot

To receive private notifications, the administrator must open the bot and send /start first. Use the numeric Telegram chat ID for ADMIN_CHAT_ID and the numeric Telegram user ID for ADMIN_USER_ID. Keep both IDs and the bot token out of source control.

## Deployment

The bot is currently deployed as a background worker on Dada Cloud using Telegram long polling. The user has confirmed that the bot responds and the main flow has been tested in Telegram.

For a new deployment:

1. Connect the GitHub repository and choose the branch to deploy.
2. Set the working directory to `telegram-business-assistant` if the platform supports monorepo subdirectory setting.
3. Select background worker mode (not a web service).
4. Configure environment variables in the platform's secret/environment settings:
   - `BOT_TOKEN` (required; never put in Git)
   - `DATABASE_PATH` (set to a path on verified persistent storage, if available)
   - `ADMIN_CHAT_ID` (optional)
   - `ADMIN_USER_ID` (optional)
5. Use the start command `python -m src.bot`.
6. Check runtime logs and test the bot flow.

**Storage warning:** The current hosted deployment has no confirmed persistent volume for SQLite. Do not collect real customer enquiries until persistence, backups and retention are verified. A container filesystem may be replaced during redeploy/rebuild. The current hosting trial is not a guarantee of permanent free hosting.

## Docker deployment

The repository includes a Dockerfile and Docker Compose configuration for a single-instance VPS deployment. The bot uses Telegram long polling and does not expose an inbound HTTP port.

1. Install Docker Engine and the Docker Compose V2 plugin on a Linux server.
2. Clone the repository and enter the project directory:

       git clone https://github.com/blvxx/portfolio.git
       cd portfolio/telegram-business-assistant

3. Create the private environment file and restrict its permissions:

       cp .env.example .env
       chmod 600 .env

4. Edit .env and set BOT_TOKEN. Start with optional ADMIN_CHAT_ID and ADMIN_USER_ID blank.
5. Build and start the container:

       docker compose up -d --build

6. Follow startup logs:

       docker compose logs -f --tail=100 bot

7. Open the bot in Telegram and send /start, then /my_id. Copy the displayed IDs into ADMIN_CHAT_ID and ADMIN_USER_ID in .env and restart:

       docker compose up -d

The Compose file stores SQLite data in a named persistent volume. It runs as a non-root user, uses a read-only container filesystem, drops Linux capabilities and restarts the process after a failure. Keep the VPS firewall closed to inbound ports other than the SSH access you administer. Do not commit .env or share the bot token.

To stop the service without deleting lead data:

       docker compose down

To remove the service and its stored data permanently (destructive):

       docker compose down -v

For a single-instance MVP this setup is sufficient. MemoryStorage keeps unfinished chat steps in process memory, so users may need to restart an unfinished request after a redeploy; saved leads remain in the persistent volume. Use Redis for shared FSM state and PostgreSQL for a multi-instance deployment.

## Tests

       pytest -q

Tests cover lead persistence, newest-first ordering, result limits, validation boundaries, application-service policy, Telegram handler orchestration, outbox transaction atomicity, concurrent claims, lease fencing, retry/dead-letter transitions, dispatcher delivery, schema migration/upgrade behaviour and repeated/concurrent Telegram submission replays. They do not require a live Telegram token or network access.

## Configuration

| Variable | Required | Purpose |
|---|---|---|
| BOT_TOKEN | Yes | Telegram Bot API token |
| DATABASE_PATH | No | SQLite file path; defaults to data/leads.sqlite3 |
| ADMIN_CHAT_ID | No | Chat that receives new enquiry notifications |
| ADMIN_USER_ID | No | User ID allowed to run /leads |

## Engineering documentation

The engineering notes distinguish the current implementation from future design proposals:

- [Current-state architecture and target design](./docs/engineering/architecture.md)
- [ADR-0001: storage and conversation state](./docs/engineering/decisions/0001-storage-and-state.md)
- [ADR-0002: transactional notification outbox](./docs/engineering/decisions/0002-transactional-notification-outbox.md)
- [ADR-0003: idempotent Telegram submissions](./docs/engineering/decisions/0003-idempotent-telegram-submissions.md)
- [Security threat model and control gaps](./docs/engineering/security/threat-model.md)
- [Operations runbook: deploy, backup and restore](./docs/engineering/operations/runbook.md)
- [Evidence-based engineering roadmap](./docs/engineering/roadmap.md)

The runbook is documentation, not proof that backup/restore has been exercised in production. The roadmap lists planned work separately from implemented capabilities.

## Security and data handling

- The bot asks for consent before collecting contact information.
- It does not request passwords, authentication codes or payment details.
- SQL statements use parameters rather than string interpolation.
- User-provided content is HTML-escaped before it is included in administrator messages.
- The /leads command is restricted to ADMIN_USER_ID and private chats.
- Outbox events store the destination chat ID and lead reference rather than duplicating contact and request fields in the event payload.
- Outbox error metadata stores exception type names, not arbitrary exception text.
- Tokens belong in environment variables or deployment secrets, never in commits.
- Define a retention period and publish a business-specific privacy notice before using this template with real customers.

## Production improvements

Before a client deployment, confirm data persistence and backups, define a privacy notice and retention policy, add monitoring, and integrate the client's CRM or messaging channel only after API/access requirements are agreed. This is a deployed portfolio MVP, not yet a hardened production service.
