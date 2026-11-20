import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from analyze_incident import analyze


class AnalyzeIncidentTests(unittest.TestCase):
    def run_analyzer(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "application.log"
            log_path.write_text(text, encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exit_code = analyze(log_path)
            return exit_code, output.getvalue()

    def test_counts_failed_and_successful_webhooks(self):
        log = (
            "2026-11-20T09:00:00Z ERROR signature_validation_failed event_id=evt1 reason=secret_mismatch\n"
            "2026-11-20T09:01:00Z INFO webhook_processed event_id=evt2 status=200\n"
        )
        code, output = self.run_analyzer(log)
        self.assertEqual(code, 0)
        self.assertIn("Failed webhook validations: 1", output)
        self.assertIn("Successfully processed webhooks: 1", output)
        self.assertIn("secret_mismatch", output)

    def test_empty_log_is_valid(self):
        code, output = self.run_analyzer("")
        self.assertEqual(code, 0)
        self.assertIn("Lines parsed: 0", output)
        self.assertIn("Failed webhook validations: 0", output)

    def test_malformed_line_is_skipped(self):
        code, output = self.run_analyzer("bad log line\n")
        self.assertEqual(code, 0)
        self.assertIn("Skipping malformed line 1", output)
        self.assertIn("Lines parsed: 0", output)

    def test_missing_file_returns_error_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing.log"
            output = io.StringIO()
            with contextlib.redirect_stderr(output):
                code = analyze(missing)
            self.assertEqual(code, 2)
            self.assertIn("Log file not found", output.getvalue())


if __name__ == "__main__":
    unittest.main()
