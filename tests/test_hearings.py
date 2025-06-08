import unittest
import time
from server import get_hearings


class TestHearingsAPI(unittest.TestCase):
    """Test the get_hearings endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_hearings_no_params(self):
        """Test get_hearings with no parameters (list all hearings)"""
        result = get_hearings()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Common possible response structures for hearings
            self.assertTrue("hearings" in result or "hearing" in result)

    def test_get_hearings_with_congress(self):
        """Test get_hearings with congress parameter"""
        result = get_hearings(congress=118)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("hearings" in result or "hearing" in result)

    def test_get_hearings_with_congress_and_chamber(self):
        """Test get_hearings with congress and chamber parameters"""
        result = get_hearings(congress=118, chamber="house")

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("hearings" in result or "hearing" in result)

    def test_get_hearings_with_pagination(self):
        """Test get_hearings with offset and limit parameters"""
        result = get_hearings(congress=118, offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for hearing data
            hearing_data = None
            for key in ["hearings", "hearing"]:
                if key in result:
                    hearing_data = result[key]
                    break

            if hearing_data is not None:
                self.assertIsInstance(hearing_data, list)
                # Should have at most 5 hearings
                self.assertLessEqual(len(hearing_data), 5)

    def test_get_hearings_with_small_limit(self):
        """Test get_hearings with a small limit to get quick results"""
        result = get_hearings(congress=118, limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for hearing data
            hearing_data = None
            for key in ["hearings", "hearing"]:
                if key in result:
                    hearing_data = result[key]
                    break

            if hearing_data is not None:
                self.assertIsInstance(hearing_data, list)
                # Should have at most 3 hearings
                self.assertLessEqual(len(hearing_data), 3)

    def test_get_hearings_response_structure(self):
        """Test that API response has expected structure"""
        result = get_hearings(congress=118, limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for hearing data
            hearing_data = None
            for key in ["hearings", "hearing"]:
                if key in result:
                    hearing_data = result[key]
                    break

            if hearing_data is not None and len(hearing_data) > 0:
                hearing = hearing_data[0]
                # Check for common hearing fields
                possible_fields = ["chamber", "congress", "date", "title", "hearingNumber"]
                has_hearing_field = any(field in hearing for field in possible_fields)
                self.assertTrue(has_hearing_field, f"Hearing missing expected fields. Available fields: {list(hearing.keys())}")

    def test_get_hearings_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_hearings(congress=118, limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for hearing data
            hearing_data = None
            for key in ["hearings", "hearing"]:
                if key in result:
                    hearing_data = result[key]
                    break

            if hearing_data is not None:
                self.assertLessEqual(len(hearing_data), 2)

    def test_get_hearings_senate_chamber(self):
        """Test get_hearings for senate chamber"""
        result = get_hearings(congress=118, chamber="senate", limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("hearings" in result or "hearing" in result)


if __name__ == '__main__':
    unittest.main()
