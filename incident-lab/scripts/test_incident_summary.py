import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from incident_summary import summarize, write_html, write_json

class IncidentSummaryTests(unittest.TestCase):
    def test_summary_detects_signature_errors_and_high_priority(self):
        with TemporaryDirectory() as temp:
            log = Path(temp) / "log.txt"
            log.write_text("2026-01-01T10:00:00Z ERROR signature_validation_failed HTTP 401 secret_mismatch\n", encoding="utf-8")
            findings = [{"severity":"HIGH","issue":"PAYMENT_ORDER_STATUS_MISMATCH","order_id":"ORD-1"}]
            result = summarize(log, findings)
        self.assertEqual(result["priority"], "HIGH")
        self.assertEqual(result["affected_order_count"], 1)
        self.assertEqual(result["log_pattern_counts"]["signature/authentication failures"], 1)
        self.assertTrue(result["recommendations"])

    def test_missing_log_is_reported_without_crashing(self):
        with TemporaryDirectory() as temp:
            log = Path(temp) / "missing.log"
            result = summarize(log, [])
        self.assertFalse(result["logs_present"])
        self.assertEqual(result["priority"], "LOW")

    def test_html_and_json_output(self):
        with TemporaryDirectory() as temp:
            log = Path(temp) / "log.txt"
            log.write_text("2026-01-01T10:00:00Z INFO webhook_processed\n", encoding="utf-8")
            result = summarize(log, [])
            html_path, json_path = Path(temp) / "summary.html", Path(temp) / "summary.json"
            write_html(result, html_path)
            write_json(result, json_path)
            self.assertIn("Incident Summary", html_path.read_text(encoding="utf-8"))
            self.assertIn('"priority": "LOW"', json_path.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
