import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from reconcile_payments import reconcile, write_html_report

class ReconciliationTests(unittest.TestCase):
    def test_detects_missing_payment(self):
        orders = [{"order_id":"A","status":"pending_payment"}]
        self.assertEqual(reconcile(orders, [] )[0]["issue"], "MISSING_PAYMENT")

    def test_successful_payment_with_pending_order(self):
        orders = [{"order_id":"A","status":"pending_payment"}]
        payments = [{"payment_id":"P1","order_id":"A","provider_payment_id":"X","status":"succeeded"}]
        issues = [f["issue"] for f in reconcile(orders, payments)]
        self.assertIn("PAYMENT_ORDER_STATUS_MISMATCH", issues)

    def test_duplicate_provider_id(self):
        orders = [{"order_id":"A","status":"paid"}]
        payments = [
            {"payment_id":"P1","order_id":"A","provider_payment_id":"X","status":"succeeded"},
            {"payment_id":"P2","order_id":"A","provider_payment_id":"X","status":"succeeded"},
        ]
        issues = [f["issue"] for f in reconcile(orders, payments)]
        self.assertIn("DUPLICATE_PROVIDER_PAYMENT_ID", issues)
        self.assertIn("MULTIPLE_PAYMENTS_FOR_ORDER", issues)

    def test_failed_payment(self):
        orders = [{"order_id":"A","status":"pending_payment"}]
        payments = [{"payment_id":"P1","order_id":"A","provider_payment_id":"X","status":"failed"}]
        self.assertIn("FAILED_PAYMENT", [f["issue"] for f in reconcile(orders, payments)])

    def test_no_findings_for_consistent_order(self):
        orders = [{"order_id":"A","status":"paid"}]
        payments = [{"payment_id":"P1","order_id":"A","provider_payment_id":"X","status":"succeeded"}]
        self.assertEqual(reconcile(orders, payments), [])

    def test_html_report_summary_and_escaping(self):
        findings = [
            {"severity":"HIGH","issue":"PAYMENT_ORDER_STATUS_MISMATCH","order_id":"A","payment_ids":"P1","details":"Mismatch <script>","recommended_action":"Check webhook"},
            {"severity":"MEDIUM","issue":"FAILED_PAYMENT","order_id":"B","payment_ids":"P2","details":"Failed","recommended_action":"Review provider"},
        ]
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "report.html"
            write_html_report(findings, path, orders_checked=3)
            html = path.read_text(encoding="utf-8")
        self.assertIn("Affected orders", html)
        self.assertIn("Issue types", html)
        self.assertIn("PAYMENT_ORDER_STATUS_MISMATCH", html)
        self.assertNotIn("<script>", html)

    def test_html_report_empty_findings(self):
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "empty.html"
            write_html_report([], path, orders_checked=0)
            html = path.read_text(encoding="utf-8")
        self.assertIn("No findings. Data appears consistent.", html)
        self.assertIn("No issues detected.", html)

    def test_multiple_payment_records_flagged(self):
        orders = [{"order_id":"A","status":"paid"}]
        payments = [
            {"payment_id":"P1","order_id":"A","provider_payment_id":"X1","status":"succeeded"},
            {"payment_id":"P2","order_id":"A","provider_payment_id":"X2","status":"succeeded"},
        ]
        self.assertIn("MULTIPLE_PAYMENTS_FOR_ORDER", [f["issue"] for f in reconcile(orders, payments)])

if __name__ == "__main__":
    unittest.main()
