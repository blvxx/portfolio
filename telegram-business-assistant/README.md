# Telegram Business Assistant

A Telegram bot starter for small businesses that need a structured way to receive and route enquiries.

The project demonstrates a complete lead-capture workflow: consent, service selection, contact validation, request description, SQLite persistence and optional administrator notifications.

## What it does

- Shows a clear entry menu and explains the available service scenarios.
- Collects explicit consent before asking for personal contact details.
- Lets a visitor choose the type of enquiry.
- Accepts a phone number, email address or Telegram shared contact.
- Validates the contact and request description.
- Stores each enquiry in SQLite with a UTC timestamp.
- Optionally notifies an administrator through ADMIN_CHAT_ID.
- Provides a restricted /leads command for an administrator configured with ADMIN_USER_ID.
- Includes /cancel to stop an unfinished request.

## Stack

- Python 3.11+
- aiogram 3.x
- aiosqlite / SQLite
- pytest and pytest-asyncio
- GitHub Actions

SQLite is intentional for a compact, easy-to-run MVP. A production deployment with multiple workers or higher throughput should use a managed database such as PostgreSQL and a persistent volume.

## Architecture

    Telegram Update
          |
          v
    aiogram Router
          |
          +---- Consent and service selection
          |
          +---- Contact and request validation
          |
          v
    Lead Service / Database
          |
          +---- SQLite lead store
          |
          +---- Optional admin notification

The bot keeps conversational state in aiogram MemoryStorage. Lead records are persisted in SQLite and survive process restarts. For a multi-instance production deployment, replace MemoryStorage with Redis or another shared FSM backend.

## Run locally

1. Use Python 3.11 or newer.
2. Create a virtual environment and install dependencies:

       python -m venv .venv
       # Windows:
       .venv\Scripts\activate
       # macOS / Linux:
       source .venv/bin/activate
       pip install -r requirements-dev.txt

3. Copy .env.example to .env.
4. Create a Telegram bot with @BotFather and place its token in BOT_TOKEN.
5. Optionally set ADMIN_CHAT_ID and ADMIN_USER_ID.
6. Start the bot:

       python -m src.bot

To receive private notifications, the administrator must open the bot and send /start first. Use the numeric Telegram chat ID for ADMIN_CHAT_ID and the numeric Telegram user ID for ADMIN_USER_ID. Keep both IDs and the bot token out of source control.

## Tests

       pytest -q

Tests cover lead persistence, newest-first ordering, result limits and validation boundaries. They do not require a live Telegram token or network access.

## Configuration

| Variable | Required | Purpose |
|---|---|---|
| BOT_TOKEN | Yes | Telegram Bot API token |
| DATABASE_PATH | No | SQLite file path; defaults to data/leads.sqlite3 |
| ADMIN_CHAT_ID | No | Chat that receives new enquiry notifications |
| ADMIN_USER_ID | No | User ID allowed to run /leads |

## Security and data handling

- The bot asks for consent before collecting contact information.
- It does not request passwords, authentication codes or payment details.
- SQL statements use parameters rather than string interpolation.
- User-provided content is HTML-escaped before it is included in administrator messages.
- The /leads command is restricted to ADMIN_USER_ID.
- Tokens belong in environment variables or deployment secrets, never in commits.
- Define a retention period and publish a business-specific privacy notice before using this template with real customers.

## Current scope and next production steps

This is a functional MVP and portfolio engineering project, not a deployed service. It does not currently connect to a live CRM, payment provider, external AI model or public business account.

For a client deployment, confirm the data fields, privacy notice and retention policy; replace SQLite if the expected load requires it; add monitoring and backups; and integrate the specific CRM or messaging channel only after the API and access requirements are agreed.
