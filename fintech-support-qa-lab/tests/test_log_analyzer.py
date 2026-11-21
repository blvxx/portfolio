import json

import pytest

from scripts.analyze_logs import load_events


def test_load_jsonl_events(tmp_path):
    log_file = tmp_path / "events.log"
    log_file.write_text(
        json.dumps({"level": "INFO", "event": "payment.created"}) + "\n"
        + json.dumps({"level": "ERROR", "event": "payment.failed"}) + "\n",
        encoding="utf-8",
    )
    events = load_events(log_file)
    assert len(events) == 2
    assert events[1]["level"] == "ERROR"


def test_load_events_reports_invalid_json(tmp_path):
    log_file = tmp_path / "broken.log"
    log_file.write_text('{"level": "INFO"}\nnot-json\n', encoding="utf-8")
    with pytest.raises(ValueError, match="line 2"):
        load_events(log_file)
