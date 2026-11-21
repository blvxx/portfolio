import unittest
from incident_ops import classify_impact

class ImpactClassificationTests(unittest.TestCase):
    def test_high_priority_is_sev2(self):
        self.assertEqual(classify_impact({"priority":"HIGH","affected_order_count":1,"finding_count":1})["severity"], "SEV-2")
    def test_three_affected_entities_is_sev2(self):
        self.assertEqual(classify_impact({"priority":"MEDIUM","affected_order_count":3,"finding_count":3})["severity"], "SEV-2")
    def test_findings_without_high_priority_is_sev3(self):
        self.assertEqual(classify_impact({"priority":"MEDIUM","affected_order_count":1,"finding_count":2})["severity"], "SEV-3")
    def test_clean_data_is_sev4(self):
        self.assertEqual(classify_impact({"priority":"LOW","affected_order_count":0,"finding_count":0})["severity"], "SEV-4")

if __name__ == "__main__":
    unittest.main()
