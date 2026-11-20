import contextlib, io, tempfile, unittest
from pathlib import Path
from analyze_incident import analyze

class PatternClassificationTests(unittest.TestCase):
    def run_analyzer(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "log.txt"
            path.write_text(text, encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = analyze(path)
            return code, out.getvalue()

    def test_classifies_known_patterns(self):
        log = (
            "2026-11-20T09:00:00Z ERROR signature_validation_failed event_id=e1\n"
            "2026-11-20T09:01:00Z WARN webhook_timeout event_id=e2\n"
            "2026-11-20T09:02:00Z ERROR downstream_5xx event_id=e3\n"
            "2026-11-20T09:03:00Z WARN duplicate_event event_id=e1\n"
            "2026-11-20T09:04:00Z WARN webhook_delayed event_id=e4\n"
            "2026-11-20T09:05:00Z INFO webhook_processed event_id=e5\n"
        )
        code, output = self.run_analyzer(log)
        self.assertEqual(code, 0)
        for phrase in ("Signature/authentication failures", "Webhook timeouts",
                       "Downstream server errors", "Duplicate deliveries",
                       "Delayed webhook deliveries", "Priority: HIGH",
                       "Successfully processed webhooks: 1"):
            self.assertIn(phrase, output)

    def test_empty_log(self):
        code, output = self.run_analyzer("")
        self.assertEqual(code, 0)
        self.assertIn("No known incident patterns detected", output)

    def test_malformed_line(self):
        code, output = self.run_analyzer("malformed\n")
        self.assertEqual(code, 0)
        self.assertIn("Malformed lines: 1", output)

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = analyze(Path(tmp) / "missing.log")
            self.assertEqual(code, 2)
            self.assertIn("Log file not found", err.getvalue())

if __name__ == "__main__":
    unittest.main()
