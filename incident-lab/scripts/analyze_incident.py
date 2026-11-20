#!/usr/bin/env python3
"""Classify fictional incident log patterns. Python 3.10+, stdlib only."""
from collections import Counter
from pathlib import Path
import re
import sys

TIMESTAMP_RE = re.compile(r"^(\S+)\s+(INFO|WARN|ERROR)\s+(.*)$")
PATTERNS = {
    "signature_validation_failed": ("Signature/authentication failures", "Check webhook secret/version and signature configuration."),
    "webhook_timeout": ("Webhook timeouts", "Check handler latency, network, dependencies, and retry policy."),
    "downstream_5xx": ("Downstream server errors", "Check downstream service health and request/error traces."),
    "duplicate_event": ("Duplicate deliveries", "Verify idempotency keys and duplicate-safe processing."),
    "webhook_delayed": ("Delayed webhook deliveries", "Inspect queue depth, consumer lag, and delivery SLA."),
}

def analyze(path: Path) -> int:
    if not path.exists():
        print(f"Log file not found: {path}", file=sys.stderr)
        return 2
    levels, events, categories = Counter(), Counter(), Counter()
    malformed = 0
    processed = 0
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = TIMESTAMP_RE.match(line)
        if not match:
            malformed += 1
            print(f"Skipping malformed line {line_number}: {line}", file=sys.stderr)
            continue
        _, level, message = match.groups()
        levels[level] += 1
        event = message.split()[0] if message else "unknown"
        events[event] += 1
        if event in PATTERNS:
            categories[event] += 1
        if event == "webhook_processed":
            processed += 1
    print("Incident Log Analysis")
    print("===================")
    print(f"Lines parsed: {sum(levels.values())}")
    print(f"Malformed lines: {malformed}")
    print(f"Log levels: {dict(levels)}")
    print(f"Successfully processed webhooks: {processed}")
    print("\nDetected patterns:")
    if not categories:
        print("  No known incident patterns detected.")
    for event, count in sorted(categories.items()):
        label, action = PATTERNS[event]
        print(f"  [{count}] {label} ({event})")
        print(f"      Suggested check: {action}")
    print("\nEvent counts:")
    for event, count in sorted(events.items()):
        print(f"  {event}: {count}")
    if categories:
        print("\nTriage recommendation:")
        if "signature_validation_failed" in categories:
            print("  Priority: HIGH — webhook authentication/configuration failures can block state updates.")
        elif "downstream_5xx" in categories or "webhook_timeout" in categories:
            print("  Priority: HIGH — check dependency availability and retry/backlog.")
        elif "duplicate_event" in categories:
            print("  Priority: MEDIUM — confirm idempotent handling and deduplication.")
        else:
            print("  Priority: MEDIUM — investigate delivery lag and queue health.")
    return 0

if __name__ == "__main__":
    default_log = Path(__file__).resolve().parents[1] / "evidence" / "application.log"
    log_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_log
    raise SystemExit(analyze(log_path))
