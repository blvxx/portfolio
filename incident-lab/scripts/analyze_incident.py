#!/usr/bin/env python3
"""Summarize the fictional Incident Investigation Lab log. Python 3.10+, stdlib only."""

from collections import Counter
from pathlib import Path
import re
import sys

TIMESTAMP_RE = re.compile(r"^(\S+)\s+(INFO|WARN|ERROR)\s+(.*)$")


def analyze(path: Path) -> int:
    if not path.exists():
        print(f"Log file not found: {path}", file=sys.stderr)
        return 2

    levels: Counter[str] = Counter()
    error_reasons: Counter[str] = Counter()
    events: Counter[str] = Counter()
    failed_webhooks = 0
    processed_webhooks = 0

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = TIMESTAMP_RE.match(line)
        if not match:
            print(f"Skipping malformed line {line_number}: {line}", file=sys.stderr)
            continue

        _, level, message = match.groups()
        levels[level] += 1

        fields = dict(re.findall(r"(\w+)=([^\s]+)", message))
        event = message.split()[0] if message else "unknown"
        events[event] += 1

        if event == "signature_validation_failed":
            failed_webhooks += 1
            error_reasons[fields.get("reason", "unspecified")] += 1
        elif event == "webhook_processed":
            processed_webhooks += 1

    print("Incident log summary")
    print("==================")
    print(f"Lines parsed: {sum(levels.values())}")
    print(f"Levels: {dict(levels)}")
    print(f"Failed webhook validations: {failed_webhooks}")
    print(f"Successfully processed webhooks: {processed_webhooks}")
    print(f"Failure reasons: {dict(error_reasons)}")
    print("Event counts:")
    for name, count in sorted(events.items()):
        print(f"  {name}: {count}")

    return 0


if __name__ == "__main__":
    default_log = Path(__file__).resolve().parents[1] / "evidence" / "application.log"
    log_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_log
    raise SystemExit(analyze(log_path))
