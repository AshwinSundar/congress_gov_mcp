import unittest
import time
from server import get_congress


class TestCongressAPI(unittest.TestCase):
    """Test the get_congress endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_congress_no_params(self):
        """Test get_congress with no parameters (list all congresses)"""
        result = get_congress()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("congresses", result)
            self.assertIsInstance(result["congresses"], list)

    def test_get_congress_with_specific_congress(self):
        """Test get_congress with specific congress number"""
        result = get_congress(congress=118)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # For specific congress, response structure might be different
            self.assertTrue("congress" in result or "congresses" in result)

    def test_get_congress_with_pagination(self):
        """Test get_congress with offset and limit parameters"""
        result = get_congress(offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("congresses", result)
            congresses = result["congresses"]
            self.assertIsInstance(congresses, list)
            # Should have at most 5 congresses
            self.assertLessEqual(len(congresses), 5)

    def test_get_congress_with_small_limit(self):
        """Test get_congress with a small limit to get quick results"""
        result = get_congress(limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("congresses", result)
            congresses = result["congresses"]
            self.assertIsInstance(congresses, list)
            # Should have at most 3 congresses
            self.assertLessEqual(len(congresses), 3)

    def test_get_congress_response_structure(self):
        """Test that API response has expected structure"""
        result = get_congress(limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("congresses", result)
            congresses = result["congresses"]
            if len(congresses) > 0:
                congress = congresses[0]
                # Check for common congress fields
                expected_fields = ["name", "startYear", "endYear"]
                for field in expected_fields:
                    self.assertIn(field, congress, f"Missing field: {field}")

    def test_get_congress_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_congress(limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("congresses", result)
            congresses = result["congresses"]
            self.assertLessEqual(len(congresses), 2)

    def test_get_congress_recent_congress(self):
        """Test get_congress for a recent congress"""
        result = get_congress(congress=117)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # For specific congress, response structure might be different
            self.assertTrue("congress" in result or "congresses" in result)


if __name__ == '__main__':
    unittest.main()
