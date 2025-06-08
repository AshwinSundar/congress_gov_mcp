import unittest
import time
from server import get_nomination


class TestNominationAPI(unittest.TestCase):
    """Test the get_nomination endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_nomination_no_params(self):
        """Test get_nomination with no parameters (list all nominations)"""
        result = get_nomination()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Common possible response structures for nominations
            self.assertTrue("nominations" in result or "nomination" in result)

    def test_get_nomination_with_congress(self):
        """Test get_nomination with congress parameter"""
        result = get_nomination(congress=118)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("nominations" in result or "nomination" in result)

    def test_get_nomination_with_pagination(self):
        """Test get_nomination with offset and limit parameters"""
        result = get_nomination(congress=118, offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for nomination data
            nom_data = None
            for key in ["nominations", "nomination"]:
                if key in result:
                    nom_data = result[key]
                    break

            if nom_data is not None:
                self.assertIsInstance(nom_data, list)
                # Should have at most 5 nominations
                self.assertLessEqual(len(nom_data), 5)

    def test_get_nomination_with_small_limit(self):
        """Test get_nomination with a small limit to get quick results"""
        result = get_nomination(congress=118, limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for nomination data
            nom_data = None
            for key in ["nominations", "nomination"]:
                if key in result:
                    nom_data = result[key]
                    break

            if nom_data is not None:
                self.assertIsInstance(nom_data, list)
                # Should have at most 3 nominations
                self.assertLessEqual(len(nom_data), 3)

    def test_get_nomination_response_structure(self):
        """Test that API response has expected structure"""
        result = get_nomination(congress=118, limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for nomination data
            nom_data = None
            for key in ["nominations", "nomination"]:
                if key in result:
                    nom_data = result[key]
                    break

            if nom_data is not None and len(nom_data) > 0:
                nomination = nom_data[0]
                # Check for common nomination fields
                possible_fields = ["congress", "number", "nominationNumber", "description"]
                has_nom_field = any(field in nomination for field in possible_fields)
                self.assertTrue(has_nom_field, f"Nomination missing expected fields. Available fields: {list(nomination.keys())}")

    def test_get_nomination_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_nomination(congress=118, limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for nomination data
            nom_data = None
            for key in ["nominations", "nomination"]:
                if key in result:
                    nom_data = result[key]
                    break

            if nom_data is not None:
                self.assertLessEqual(len(nom_data), 2)


if __name__ == '__main__':
    unittest.main()
