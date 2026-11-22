from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB_ROOT))

from scripts.log_triage import analyze_lines, main


class AnalyzeLinesTests(unittest.TestCase):
    def test_detects_known_patterns_and_prioritizes_severity(self):
        findings = analyze_lines([
            "host app[1]: connection refused",
            "host kernel: Out of memory: Killed process 412",
            "host nginx: upstream timed out",
        ], source="fixture.log")
        self.assertEqual(
            [item["rule_id"] for item in findings],
            ["OOM_KILL", "NGINX_UPSTREAM_TIMEOUT", "CONNECTION_REFUSED"],
        )

    def test_only_one_rule_is_returned_for_a_line(self):
        findings = analyze_lines(["upstream connect() failed (111: Connection refused)"])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule_id"], "NGINX_UPSTREAM_REFUSED")

    def test_unknown_lines_are_ignored(self):
        self.assertEqual(analyze_lines(["service started successfully"]), [])

    def test_preserves_source_and_line_number(self):
        findings = analyze_lines(["ok", "No space left on device"], "var.log")
        self.assertEqual(findings[0]["source"], "var.log")
        self.assertEqual(findings[0]["line_number"], 2)


class CliTests(unittest.TestCase):
    def test_json_output_contains_findings(self):
        from io import StringIO
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.log"
            path.write_text("app: Temporary failure in name resolution
", encoding="utf-8")
            output = StringIO()
            original_stdout = sys.stdout
            try:
                sys.stdout = output
                code = main([str(path), "--format", "json"])
            finally:
                sys.stdout = original_stdout
        parsed = json.loads(output.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(parsed["finding_count"], 1)
        self.assertEqual(parsed["findings"][0]["rule_id"], "DNS_FAILURE")

    def test_missing_file_returns_nonzero_and_json_error(self):
        from io import StringIO
        output = StringIO()
        original_stdout = sys.stdout
        try:
            sys.stdout = output
            code = main(["definitely-missing-lab-log.txt", "--format", "json"])
        finally:
            sys.stdout = original_stdout
        parsed = json.loads(output.getvalue())
        self.assertEqual(code, 2)
        self.assertEqual(len(parsed["errors"]), 1)


if __name__ == "__main__":
    unittest.main()
