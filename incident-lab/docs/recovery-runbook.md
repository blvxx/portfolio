# Recovery Runbook — Payment Webhook 401

## Preconditions
- Incident owner identified.
- Provider event IDs and affected order IDs collected.
- Access is through approved, least-privilege tooling.
- Secret values are not copied into tickets, chat, terminal history, or logs.
- Database changes/replays require review and a backup/rollback plan.

## Procedure

### 1. Confirm incident scope
- Check webhook 4xx rate and time window.
- Confirm the endpoint and environment.
- Collect provider event IDs, timestamps, and affected order IDs.

### 2. Validate configuration
- Confirm secret reference/version with the authorized secrets manager.
- Do not reveal or log the secret value.
- Check recent rotation/deployment changes.
- Verify handler uses the expected signing algorithm and raw body.

### 3. Test safely
- Use provider test mode or a controlled test event.
- Confirm valid event receives expected 2xx response.
- Confirm invalid signature still receives 401.
- Verify event is recorded and state transition occurs once.

### 4. Reconcile business data
- Identify successful provider payments with orders not marked paid.
- Confirm no duplicate payment records or conflicting transitions.
- Prepare an affected-order list for review.

### 5. Replay / recovery
- Replay only eligible failed events using approved tooling.
- Ensure idempotency by provider event ID and payment/order IDs.
- Do not initiate new charges as a recovery action.
- Monitor processing and record results.

### 6. Verify closure
- Webhook 401 rate is back to baseline.
- Valid events process; invalid signatures remain rejected.
- Reconciliation mismatch count is zero for the incident scope.
- No duplicate transitions or payment records.
- Stakeholders updated; incident and RCA documented.

## Rollback / escalation
If the corrected configuration fails validation or causes unexpected state changes, stop replay, revert the configuration using the approved change process, preserve evidence, and escalate to the payments/integration owner.
