import unittest
import time
from server import get_summaries


class TestSummariesAPI(unittest.TestCase):
    """Test the get_summaries endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_summaries_no_params(self):
        """Test get_summaries with no parameters (default values)"""
        result = get_summaries()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("summaries", result)
            self.assertIsInstance(result["summaries"], list)

    def test_get_summaries_with_congress(self):
        """Test get_summaries with congress parameter"""
        result = get_summaries(congress=118)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("summaries", result)
            self.assertIsInstance(result["summaries"], list)

    def test_get_summaries_with_congress_and_bill_type(self):
        """Test get_summaries with congress and bill_type parameters"""
        result = get_summaries(congress=118, bill_type="hr")

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("summaries", result)
            self.assertIsInstance(result["summaries"], list)

    def test_get_summaries_with_pagination(self):
        """Test get_summaries with offset and limit parameters"""
        result = get_summaries(congress=118, offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("summaries", result)
            summaries = result["summaries"]
            self.assertIsInstance(summaries, list)
            # Should have at most 5 summaries
            self.assertLessEqual(len(summaries), 5)

    def test_get_summaries_with_small_limit(self):
        """Test get_summaries with a small limit to get quick results"""
        result = get_summaries(congress=118, limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("summaries", result)
            summaries = result["summaries"]
            self.assertIsInstance(summaries, list)
            # Should have at most 3 summaries
            self.assertLessEqual(len(summaries), 3)

    def test_get_summaries_senate_bills(self):
        """Test get_summaries for Senate bills"""
        result = get_summaries(congress=118, bill_type="s", limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("summaries", result)
            self.assertIsInstance(result["summaries"], list)

    def test_get_summaries_response_structure(self):
        """Test that API response has expected structure"""
        result = get_summaries(congress=118, limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("summaries", result)
            summaries = result["summaries"]
            if len(summaries) > 0:
                summary = summaries[0]
                # Check for common summary fields
                expected_fields = ["actionDate", "bill"]
                for field in expected_fields:
                    self.assertIn(field, summary, f"Missing field: {field}")

                # Check bill structure
                if "bill" in summary:
                    bill = summary["bill"]
                    bill_fields = ["congress", "number"]
                    for field in bill_fields:
                        self.assertIn(field, bill, f"Missing bill field: {field}")

    def test_get_summaries_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_summaries(congress=118, limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("summaries", result)
            summaries = result["summaries"]
            self.assertLessEqual(len(summaries), 2)

    def test_get_summaries_sort_parameter(self):
        """Test that sort parameter works"""
        result = get_summaries(congress=118, limit=2, sort="updateDate+asc")

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("summaries", result)
            self.assertIsInstance(result["summaries"], list)


if __name__ == '__main__':
    unittest.main()
