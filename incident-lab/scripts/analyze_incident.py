#!/usr/bin/env python3
"""Classify fictional incident log patterns. Python 3.10+, stdlib only."""
from collections import Counter
from pathlib import Path
import re
import sys

TIMESTAMP_RE = re.compile(r"^(\S+)\s+(INFO|WARN|ERROR)\s+(.*)$")
REASON_RE = re.compile(r"\breason=([A-Za-z0-9_.-]+)")
PATTERNS = {
    "signature_validation_failed": (
        "Signature/authentication failures",
        "Check webhook secret/version and signature configuration.",
    ),
    "webhook_timeout": (
        "Webhook timeouts",
        "Check handler latency, network, dependencies, and retry policy.",
    ),
    "downstream_5xx": (
        "Downstream server errors",
        "Check downstream service health and request/error traces.",
    ),
    "duplicate_event": (
        "Duplicate deliveries",
        "Verify idempotency keys and duplicate-safe processing.",
    ),
    "webhook_delayed": (
        "Delayed webhook deliveries",
        "Inspect queue depth, consumer lag, and delivery SLA.",
    ),
}


def analyze(path: Path) -> int:
    """Print a concise, evidence-oriented summary and return a CLI exit code."""
    if not path.exists():
        print(f"Log file not found: {path}", file=sys.stderr)
        return 2

    levels: Counter[str] = Counter()
    events: Counter[str] = Counter()
    categories: Counter[str] = Counter()
    malformed_lines: list[int] = []
    failure_reasons: Counter[str] = Counter()
    processed = 0

    for line_number, line in enumerate(
        path.read_text(encoding="utf-8", errors="replace").splitlines(),
        start=1,
    ):
        match = TIMESTAMP_RE.match(line)
        if not match:
            malformed_lines.append(line_number)
            continue

        _, level, message = match.groups()
        levels[level] += 1
        event = message.split(maxsplit=1)[0] if message else "unknown"
        events[event] += 1

        if event in PATTERNS:
            categories[event] += 1
        if event == "webhook_processed":
            processed += 1
        if event == "signature_validation_failed":
            reason_match = REASON_RE.search(message)
            if reason_match:
                failure_reasons[reason_match.group(1)] += 1

    failed_validations = categories["signature_validation_failed"]

    print("Incident Log Analysis")
    print("===================")
    print(f"Lines parsed: {sum(levels.values())}")
    print(f"Malformed lines: {len(malformed_lines)}")
    for line_number in malformed_lines:
        # Do not echo the full malformed line: it may contain sensitive log data.
        print(f"Skipping malformed line {line_number}")
    print(f"Log levels: {dict(levels)}")
    print(f"Failed webhook validations: {failed_validations}")
    print(f"Successfully processed webhooks: {processed}")

    if failure_reasons:
        print("Failure reasons:")
        for reason, count in sorted(failure_reasons.items()):
            print(f"  {reason}: {count}")

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
            print(
                "  Priority: HIGH — webhook authentication/configuration "
                "failures can block state updates."
            )
        elif "downstream_5xx" in categories or "webhook_timeout" in categories:
            print(
                "  Priority: HIGH — check dependency availability and "
                "retry/backlog."
            )
        elif "duplicate_event" in categories:
            print(
                "  Priority: MEDIUM — confirm idempotent handling and "
                "deduplication."
            )
        else:
            print(
                "  Priority: MEDIUM — investigate delivery lag and queue health."
            )

    return 0


if __name__ == "__main__":
    default_log = Path(__file__).resolve().parents[1] / "evidence" / "application.log"
    log_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_log
    raise SystemExit(analyze(log_path))
