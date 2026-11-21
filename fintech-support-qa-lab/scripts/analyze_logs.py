"""Small JSONL log analyzer for the synthetic support lab dataset."""

import argparse
import json
from collections import Counter
from pathlib import Path


def load_events(path: Path) -> list[dict]:
    events = []
    with path.open(encoding="utf-8") as log_file:
        for line_number, line in enumerate(log_file, start=1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
            if not isinstance(event, dict):
                raise ValueError(f"Expected a JSON object on line {line_number}")
            events.append(event)
    return events


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize JSONL payment API logs")
    parser.add_argument(
        "logfile",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "samples" / "payment-api.log",
    )
    parser.add_argument("--correlation-id", help="Show only events for this correlation ID")
    parser.add_argument("--level", help="Filter by log level, e.g. ERROR or WARNING")
    args = parser.parse_args()

    events = load_events(args.logfile)
    if args.correlation_id:
        events = [e for e in events if e.get("correlation_id") == args.correlation_id]
    if args.level:
        events = [e for e in events if str(e.get("level", "")).upper() == args.level.upper()]

    print(f"Events: {len(events)}")
    print("By level:")
    for level, count in sorted(Counter(e.get("level", "UNKNOWN") for e in events).items()):
        print(f"  {level}: {count}")
    print("Events:")
    for event in events:
        print(
            f"  {event.get('timestamp', '-')} "
            f"{event.get('level', 'UNKNOWN'):7} "
            f"{event.get('correlation_id', '-'):12} "
            f"{event.get('event', '-')}"
        )


if __name__ == "__main__":
    main()
