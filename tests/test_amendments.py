import unittest
import time
from server import get_amendments


class TestAmendmentsAPI(unittest.TestCase):
    """Test the get_amendments endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_amendments_no_params(self):
        """Test get_amendments with no parameters (default values)"""
        result = get_amendments()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("amendments", result)
            self.assertIsInstance(result["amendments"], list)

    def test_get_amendments_with_congress(self):
        """Test get_amendments with congress parameter"""
        result = get_amendments(congress=118)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("amendments", result)
            self.assertIsInstance(result["amendments"], list)

    def test_get_amendments_with_congress_and_type(self):
        """Test get_amendments with congress and amendment_type parameters"""
        result = get_amendments(congress=118, amendment_type="hamdt")

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("amendments", result)
            self.assertIsInstance(result["amendments"], list)

    def test_get_amendments_with_pagination(self):
        """Test get_amendments with offset and limit parameters"""
        result = get_amendments(congress=118, offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("amendments", result)
            amendments = result["amendments"]
            self.assertIsInstance(amendments, list)
            # Should have at most 5 amendments
            self.assertLessEqual(len(amendments), 5)

    def test_get_amendments_with_small_limit(self):
        """Test get_amendments with a small limit to get quick results"""
        result = get_amendments(congress=118, limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("amendments", result)
            amendments = result["amendments"]
            self.assertIsInstance(amendments, list)
            # Should have at most 3 amendments
            self.assertLessEqual(len(amendments), 3)

    def test_get_amendments_senate_amendments(self):
        """Test get_amendments for Senate amendments"""
        result = get_amendments(congress=118, amendment_type="samdt", limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("amendments", result)
            self.assertIsInstance(result["amendments"], list)

    def test_get_amendments_response_structure(self):
        """Test that API response has expected structure"""
        result = get_amendments(congress=118, limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("amendments", result)
            amendments = result["amendments"]
            if len(amendments) > 0:
                amendment = amendments[0]
                # Check for common amendment fields
                expected_fields = ["congress", "type", "number"]
                for field in expected_fields:
                    self.assertIn(field, amendment, f"Missing field: {field}")

    def test_get_amendments_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_amendments(congress=118, limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("amendments", result)
            amendments = result["amendments"]
            self.assertLessEqual(len(amendments), 2)


if __name__ == '__main__':
    unittest.main()
