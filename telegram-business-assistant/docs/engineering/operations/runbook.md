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

After an update, test the bot in Telegram with a non-sensitive demo enquiry. Confirm the confirmation flow and, when configured, that the outbox event moves to delivered after the administrator message is accepted by Telegram.

## Routine health checks

    docker compose ps
    docker compose logs --since=15m bot

Check for repeated process restarts, Telegram polling/authentication errors, database open/write errors, administrator notification failures and unexpected spikes in log volume.

The current application does not expose a dedicated health endpoint or metrics endpoint.

## Notification outbox inspection

The worker polls the SQLite outbox while the bot process is running. Events move through pending, processing, delivered or dead states. Failed sends are retried with bounded exponential backoff; after five attempts an event is placed in dead state for operator review.

Inspect event counts:

    docker compose exec -T bot python -c "import sqlite3; c=sqlite3.connect('/app/data/leads.sqlite3'); print(c.execute('SELECT status, COUNT(*) FROM notification_outbox GROUP BY status').fetchall())"

Inspect recent failed/dead event metadata (this excludes lead content):

    docker compose exec -T bot python -c "import sqlite3; c=sqlite3.connect('/app/data/leads.sqlite3'); print(c.execute('SELECT id, aggregate_id, status, attempts, last_error, created_at FROM notification_outbox WHERE status IN (\'pending\', \'dead\') ORDER BY id DESC LIMIT 20').fetchall())"

A dead event should be reviewed before replay. Confirm that the configured Telegram chat is correct and that the failure is transient. Do not repeatedly requeue permanent failures.

After correcting the cause, an operator may requeue one reviewed event by its numeric event ID:

    docker compose exec -T bot python -c "import sqlite3, sys; event_id=int(sys.argv[1]); c=sqlite3.connect('/app/data/leads.sqlite3'); cur=c.execute(\"UPDATE notification_outbox SET status='pending', attempts=0, available_at=strftime('%Y-%m-%dT%H:%M:%S+00:00','now'), locked_at=NULL, lease_token=NULL, last_error=NULL WHERE id=? AND status='dead'\", (event_id,)); c.commit(); print('requeued' if cur.rowcount == 1 else 'no dead event updated')" EVENT_ID

Replace EVENT_ID with the reviewed numeric outbox ID. This operation is intentionally manual and must be performed only after checking the destination and cause. Remote delivery is at-least-once: a crash after Telegram accepts a message but before the local delivered marker is committed can result in a duplicate notification.

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
- Notification delivery is at-least-once; duplicates are possible if the process crashes after a successful remote send but before marking the event delivered.
- Dead-letter events require operator review; no automated alerting or admin replay command is provided.
- The hosted Dada Cloud storage behaviour is not verified by this runbook.
- Backup/restore commands are documented but must be exercised on a disposable test environment before being treated as an operationally proven procedure.
