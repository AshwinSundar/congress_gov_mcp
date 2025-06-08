import unittest
import time
from server import get_house_requirement


class TestHouseRequirementAPI(unittest.TestCase):
    """Test the get_house_requirement endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_house_requirement_no_params(self):
        """Test get_house_requirement with no parameters (list all requirements)"""
        result = get_house_requirement()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Common possible response structures for house requirements
            self.assertTrue("houseRequirements" in result or "requirements" in result or "houseRequirement" in result)

    def test_get_house_requirement_with_congress(self):
        """Test get_house_requirement with congress parameter"""
        result = get_house_requirement(congress=118)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("houseRequirements" in result or "requirements" in result or "houseRequirement" in result)

    def test_get_house_requirement_with_pagination(self):
        """Test get_house_requirement with offset and limit parameters"""
        result = get_house_requirement(congress=118, offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for requirement data
            req_data = None
            for key in ["houseRequirements", "requirements", "houseRequirement"]:
                if key in result:
                    req_data = result[key]
                    break
            
            if req_data is not None:
                self.assertIsInstance(req_data, list)
                # Should have at most 5 requirements
                self.assertLessEqual(len(req_data), 5)

    def test_get_house_requirement_with_small_limit(self):
        """Test get_house_requirement with a small limit to get quick results"""
        result = get_house_requirement(congress=118, limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for requirement data
            req_data = None
            for key in ["houseRequirements", "requirements", "houseRequirement"]:
                if key in result:
                    req_data = result[key]
                    break
            
            if req_data is not None:
                self.assertIsInstance(req_data, list)
                # Should have at most 3 requirements
                self.assertLessEqual(len(req_data), 3)

    def test_get_house_requirement_response_structure(self):
        """Test that API response has expected structure"""
        result = get_house_requirement(congress=118, limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for requirement data
            req_data = None
            for key in ["houseRequirements", "requirements", "houseRequirement"]:
                if key in result:
                    req_data = result[key]
                    break
            
            if req_data is not None and len(req_data) > 0:
                requirement = req_data[0]
                # Check for common requirement fields
                possible_fields = ["congress", "number", "title", "requirementNumber"]
                has_req_field = any(field in requirement for field in possible_fields)
                self.assertTrue(has_req_field, f"Requirement missing expected fields. Available fields: {list(requirement.keys())}")

    def test_get_house_requirement_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_house_requirement(congress=118, limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for requirement data
            req_data = None
            for key in ["houseRequirements", "requirements", "houseRequirement"]:
                if key in result:
                    req_data = result[key]
                    break
            
            if req_data is not None:
                self.assertLessEqual(len(req_data), 2)


if __name__ == '__main__':
    unittest.main()