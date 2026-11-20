import contextlib, io, tempfile, unittest
from pathlib import Path
from analyze_incident import analyze

class PatternClassificationTests(unittest.TestCase):
    def test_classifies_known_patterns(self):
        lines = (
            "2026-11-20T09:00:00Z ERROR signature_validation_failed event_id=e1\n"
            "2026-11-20T09:01:00Z WARN webhook_timeout event_id=e2\n"
            "2026-11-20T09:02:00Z ERROR downstream_5xx event_id=e3\n"
            "2026-11-20T09:03:00Z WARN duplicate_event event_id=e1\n"
            "2026-11-20T09:04:00Z WARN webhook_delayed event_id=e4\n"
            "2026-11-20T09:05:00Z INFO webhook_processed event_id=e5\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "log.txt"
            path.write_text(lines, encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(analyze(path), 0)
            output = out.getvalue()
            for phrase in ("Signature/authentication failures", "Webhook timeouts",
                           "Downstream server errors", "Duplicate deliveries",
                           "Delayed webhook deliveries", "Priority: HIGH",
                           "Successfully processed webhooks: 1"):
                self.assertIn(phrase, output)

    def test_empty_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.log"
            path.write_text("", encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(analyze(path), 0)
            self.assertIn("No known incident patterns detected", out.getvalue())

if __name__ == "__main__":
    unittest.main()
