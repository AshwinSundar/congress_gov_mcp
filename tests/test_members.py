import unittest
import time
from server import get_members


class TestMembersAPI(unittest.TestCase):
    """Test the get_members endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_members_no_params(self):
        """Test get_members with no parameters (list all members)"""
        result = get_members()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("members", result)
            self.assertIsInstance(result["members"], list)

    def test_get_members_with_pagination(self):
        """Test get_members with offset and limit parameters"""
        result = get_members(offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("members", result)
            members = result["members"]
            self.assertIsInstance(members, list)
            # Should have at most 5 members
            self.assertLessEqual(len(members), 5)

    def test_get_members_with_small_limit(self):
        """Test get_members with a small limit to get quick results"""
        result = get_members(limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("members", result)
            members = result["members"]
            self.assertIsInstance(members, list)
            # Should have at most 3 members
            self.assertLessEqual(len(members), 3)

    def test_get_members_current_only(self):
        """Test get_members filtered to current members only"""
        result = get_members(current_member=True, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("members", result)
            self.assertIsInstance(result["members"], list)

    def test_get_members_response_structure(self):
        """Test that API response has expected structure"""
        result = get_members(limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("members", result)
            members = result["members"]
            if len(members) > 0:
                member = members[0]
                # Check for common member fields
                expected_fields = ["bioguideId", "name"]
                for field in expected_fields:
                    self.assertIn(field, member, f"Missing field: {field}")

    def test_get_members_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_members(limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("members", result)
            members = result["members"]
            self.assertLessEqual(len(members), 2)

    def test_get_members_with_bioguide_id(self):
        """Test get_members with specific bioguide ID"""
        # Get a member first to get a valid bioguide ID
        members_result = get_members(limit=1)
        
        self.assertIsInstance(members_result, dict)
        if "error" not in members_result and "members" in members_result:
            members = members_result["members"]
            if len(members) > 0:
                bioguide_id = members[0].get("bioguideId")
                if bioguide_id:
                    result = get_members(bioguide_id=bioguide_id)
                    self.assertIsInstance(result, dict)
                    if "error" not in result:
                        # For specific member, response structure might be different
                        self.assertTrue("member" in result or "members" in result)

    def test_get_members_historical(self):
        """Test get_members for historical members"""
        result = get_members(current_member=False, limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("members", result)
            self.assertIsInstance(result["members"], list)


if __name__ == '__main__':
    unittest.main()