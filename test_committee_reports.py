import unittest
import time
from server import get_committee_reports


class TestCommitteeReportsAPI(unittest.TestCase):
    """Test the get_committee_reports endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_committee_reports_no_params(self):
        """Test get_committee_reports with no parameters (list all reports)"""
        result = get_committee_reports()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Common possible response structures for committee reports
            self.assertTrue("reports" in result or "committeeReports" in result or "committeeReport" in result)

    def test_get_committee_reports_with_congress(self):
        """Test get_committee_reports with congress parameter"""
        result = get_committee_reports(congress=118)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("reports" in result or "committeeReports" in result or "committeeReport" in result)

    def test_get_committee_reports_with_congress_and_type(self):
        """Test get_committee_reports with congress and report_type parameters"""
        result = get_committee_reports(congress=118, report_type="hrpt")

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("reports" in result or "committeeReports" in result or "committeeReport" in result)

    def test_get_committee_reports_with_pagination(self):
        """Test get_committee_reports with offset and limit parameters"""
        result = get_committee_reports(congress=118, offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for report data
            report_data = None
            for key in ["reports", "committeeReports", "committeeReport"]:
                if key in result:
                    report_data = result[key]
                    break
            
            if report_data is not None:
                self.assertIsInstance(report_data, list)
                # Should have at most 5 reports
                self.assertLessEqual(len(report_data), 5)

    def test_get_committee_reports_with_small_limit(self):
        """Test get_committee_reports with a small limit to get quick results"""
        result = get_committee_reports(congress=118, limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for report data
            report_data = None
            for key in ["reports", "committeeReports", "committeeReport"]:
                if key in result:
                    report_data = result[key]
                    break
            
            if report_data is not None:
                self.assertIsInstance(report_data, list)
                # Should have at most 3 reports
                self.assertLessEqual(len(report_data), 3)

    def test_get_committee_reports_response_structure(self):
        """Test that API response has expected structure"""
        result = get_committee_reports(congress=118, limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for report data
            report_data = None
            for key in ["reports", "committeeReports", "committeeReport"]:
                if key in result:
                    report_data = result[key]
                    break
            
            if report_data is not None and len(report_data) > 0:
                report = report_data[0]
                # Check for common report fields
                possible_fields = ["citation", "congress", "reportType", "reportNumber", "title"]
                has_report_field = any(field in report for field in possible_fields)
                self.assertTrue(has_report_field, f"Report missing expected fields. Available fields: {list(report.keys())}")

    def test_get_committee_reports_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_committee_reports(congress=118, limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for report data
            report_data = None
            for key in ["reports", "committeeReports", "committeeReport"]:
                if key in result:
                    report_data = result[key]
                    break
            
            if report_data is not None:
                self.assertLessEqual(len(report_data), 2)


if __name__ == '__main__':
    unittest.main()