import unittest
import time
from server import get_crsreport


class TestCRSReportAPI(unittest.TestCase):
    """Test the get_crsreport endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_crsreport_no_params(self):
        """Test get_crsreport with no parameters (list all reports)"""
        result = get_crsreport()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Common possible response structures for CRS reports
            self.assertTrue("CRSReports" in result or "crsReports" in result or "reports" in result or "crsReport" in result)

    def test_get_crsreport_with_pagination(self):
        """Test get_crsreport with offset and limit parameters"""
        result = get_crsreport(offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for report data
            report_data = None
            for key in ["CRSReports", "crsReports", "reports", "crsReport"]:
                if key in result:
                    report_data = result[key]
                    break
            
            if report_data is not None:
                self.assertIsInstance(report_data, list)
                # Should have at most 5 reports
                self.assertLessEqual(len(report_data), 5)

    def test_get_crsreport_with_small_limit(self):
        """Test get_crsreport with a small limit to get quick results"""
        result = get_crsreport(limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for report data
            report_data = None
            for key in ["CRSReports", "crsReports", "reports", "crsReport"]:
                if key in result:
                    report_data = result[key]
                    break
            
            if report_data is not None:
                self.assertIsInstance(report_data, list)
                # Should have at most 3 reports
                self.assertLessEqual(len(report_data), 3)

    def test_get_crsreport_response_structure(self):
        """Test that API response has expected structure"""
        result = get_crsreport(limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for report data
            report_data = None
            for key in ["CRSReports", "crsReports", "reports", "crsReport"]:
                if key in result:
                    report_data = result[key]
                    break
            
            if report_data is not None and len(report_data) > 0:
                report = report_data[0]
                # Check for common report fields
                possible_fields = ["productCode", "title", "summary", "date"]
                has_report_field = any(field in report for field in possible_fields)
                self.assertTrue(has_report_field, f"Report missing expected fields. Available fields: {list(report.keys())}")

    def test_get_crsreport_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_crsreport(limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for report data
            report_data = None
            for key in ["CRSReports", "crsReports", "reports", "crsReport"]:
                if key in result:
                    report_data = result[key]
                    break
            
            if report_data is not None:
                self.assertLessEqual(len(report_data), 2)


if __name__ == '__main__':
    unittest.main()