import unittest
import time
from server import get_treaty


class TestTreatyAPI(unittest.TestCase):
    """Test the get_treaty endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_treaty_no_params(self):
        """Test get_treaty with no parameters (list all treaties)"""
        result = get_treaty()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Common possible response structures for treaties
            self.assertTrue("treaties" in result or "treaty" in result)

    def test_get_treaty_with_congress(self):
        """Test get_treaty with congress parameter"""
        result = get_treaty(congress=118)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("treaties" in result or "treaty" in result)

    def test_get_treaty_with_pagination(self):
        """Test get_treaty with offset and limit parameters"""
        result = get_treaty(congress=118, offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for treaty data
            treaty_data = None
            for key in ["treaties", "treaty"]:
                if key in result:
                    treaty_data = result[key]
                    break

            if treaty_data is not None:
                self.assertIsInstance(treaty_data, list)
                # Should have at most 5 treaties
                self.assertLessEqual(len(treaty_data), 5)

    def test_get_treaty_with_small_limit(self):
        """Test get_treaty with a small limit to get quick results"""
        result = get_treaty(congress=118, limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for treaty data
            treaty_data = None
            for key in ["treaties", "treaty"]:
                if key in result:
                    treaty_data = result[key]
                    break

            if treaty_data is not None:
                self.assertIsInstance(treaty_data, list)
                # Should have at most 3 treaties
                self.assertLessEqual(len(treaty_data), 3)

    def test_get_treaty_response_structure(self):
        """Test that API response has expected structure"""
        result = get_treaty(congress=118, limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for treaty data
            treaty_data = None
            for key in ["treaties", "treaty"]:
                if key in result:
                    treaty_data = result[key]
                    break

            if treaty_data is not None and len(treaty_data) > 0:
                treaty = treaty_data[0]
                # Check for common treaty fields
                possible_fields = ["congress", "number", "treatyNumber", "title"]
                has_treaty_field = any(field in treaty for field in possible_fields)
                self.assertTrue(has_treaty_field, f"Treaty missing expected fields. Available fields: {list(treaty.keys())}")

    def test_get_treaty_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_treaty(congress=118, limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for treaty data
            treaty_data = None
            for key in ["treaties", "treaty"]:
                if key in result:
                    treaty_data = result[key]
                    break

            if treaty_data is not None:
                self.assertLessEqual(len(treaty_data), 2)


if __name__ == '__main__':
    unittest.main()
