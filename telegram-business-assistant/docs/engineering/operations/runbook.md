# Operations runbook

## Scope

This runbook covers the single-instance Docker Compose deployment in this repository. It does not certify the separate Dada Cloud worker's persistence or operational guarantees.

## Prerequisites

- Linux host with Docker Engine and Docker Compose V2.
- Repository checked out at a reviewed commit.
- Environment file created on the host with a valid BOT_TOKEN.
- File permissions on the environment file restricted to the deployment operator.
- A verified persistent volume for /app/data before any real personal data is collected.

Never paste bot tokens into shell transcripts, issues, screenshots or chat messages.

## Deploy or update

From the telegram-business-assistant directory:

    docker compose config
    docker compose up -d --build
    docker compose ps
    docker compose logs --tail=100 bot

After an update, test the bot in Telegram with a non-sensitive demo enquiry. Confirm the confirmation flow and, when configured, administrator notification.

## Routine health checks

    docker compose ps
    docker compose logs --since=15m bot

Check for repeated process restarts, Telegram polling/authentication errors, database open/write errors, administrator notification failures and unexpected spikes in log volume.

The current application does not expose a dedicated health endpoint or metrics endpoint.

## Backup

The Compose deployment uses the named volume mounted at /app/data. The application container is read-only except for its data volume and temporary filesystem.

For a simple backup, use SQLite's online backup API from inside the container:

    mkdir -p backups
    docker compose exec -T bot python -c "import sqlite3; src=sqlite3.connect('/app/data/leads.sqlite3'); dst=sqlite3.connect('/tmp/leads-backup.sqlite3'); src.backup(dst); dst.close(); src.close()"
    docker compose cp bot:/tmp/leads-backup.sqlite3 ./backups/leads-backup.sqlite3

Protect the resulting backup as personal data. Store it outside the application host with access controls and an agreed retention period. Do not commit backups to Git.

## Restore (destructive)

Perform restore only after confirming the correct backup and notifying the operator. The following replaces the active database.

    docker compose stop bot
    docker compose cp ./backups/leads-backup.sqlite3 bot:/tmp/leads-restore.sqlite3
    docker compose exec -T bot python -c "import sqlite3; src=sqlite3.connect('/tmp/leads-restore.sqlite3'); dst=sqlite3.connect('/app/data/leads.sqlite3'); src.backup(dst); dst.close(); src.close()"
    docker compose start bot
    docker compose logs --tail=100 bot

Validate the restored database with a test copy before using this procedure on important data. A formal recovery process still needs documented recovery point and recovery time objectives.

## Restart and shutdown

    docker compose restart bot
    docker compose down

Do not use docker compose down -v unless intentionally deleting the named database volume.

## Known limitations

- No metrics/alerting integration is included.
- FSM state is in memory and disappears on restart.
- Administrator notifications are not retried after a send failure.
- The hosted Dada Cloud storage behaviour is not verified by this runbook.
- Backup/restore commands are documented but must be exercised on a disposable test environment before being treated as an operationally proven procedure.
