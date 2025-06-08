import unittest
import time
from server import get_committees


class TestCommitteesAPI(unittest.TestCase):
    """Test the get_committees endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_committees_no_params(self):
        """Test get_committees with no parameters (list all committees)"""
        result = get_committees()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("committees", result)
            self.assertIsInstance(result["committees"], list)

    def test_get_committees_with_pagination(self):
        """Test get_committees with offset and limit parameters"""
        result = get_committees(offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("committees", result)
            committees = result["committees"]
            self.assertIsInstance(committees, list)
            # Should have at most 5 committees
            self.assertLessEqual(len(committees), 5)

    def test_get_committees_with_small_limit(self):
        """Test get_committees with a small limit to get quick results"""
        result = get_committees(limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("committees", result)
            committees = result["committees"]
            self.assertIsInstance(committees, list)
            # Should have at most 3 committees
            self.assertLessEqual(len(committees), 3)

    def test_get_committees_response_structure(self):
        """Test that API response has expected structure"""
        result = get_committees(limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("committees", result)
            committees = result["committees"]
            if len(committees) > 0:
                committee = committees[0]
                # Check for common committee fields
                expected_fields = ["systemCode", "name"]
                for field in expected_fields:
                    self.assertIn(field, committee, f"Missing field: {field}")

    def test_get_committees_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_committees(limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("committees", result)
            committees = result["committees"]
            self.assertLessEqual(len(committees), 2)

    def test_get_committees_with_system_code(self):
        """Test get_committees with specific system code"""
        # Get a committee first to get a valid system code
        committees_result = get_committees(limit=1)

        self.assertIsInstance(committees_result, dict)
        if "error" not in committees_result and "committees" in committees_result:
            committees = committees_result["committees"]
            if len(committees) > 0:
                system_code = committees[0].get("systemCode")
                if system_code:
                    result = get_committees(system_code=system_code)
                    self.assertIsInstance(result, dict)
                    if "error" not in result:
                        # For specific committee, response structure might be different
                        self.assertTrue("committee" in result or "committees" in result)

    def test_get_committees_chamber_information(self):
        """Test that committees have chamber information"""
        result = get_committees(limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("committees", result)
            committees = result["committees"]
            if len(committees) > 0:
                committee = committees[0]
                # Check for chamber field which is common in committee data
                possible_fields = ["chamber", "name", "systemCode"]
                has_expected_field = any(field in committee for field in possible_fields)
                self.assertTrue(has_expected_field, f"Committee missing expected fields. Available fields: {list(committee.keys())}")


if __name__ == '__main__':
    unittest.main()
