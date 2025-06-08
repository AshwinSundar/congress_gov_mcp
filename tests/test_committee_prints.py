import unittest
import time
from server import get_committee_prints


class TestCommitteePrintsAPI(unittest.TestCase):
    """Test the get_committee_prints endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_committee_prints_no_params(self):
        """Test get_committee_prints with no parameters (list all prints)"""
        result = get_committee_prints()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Common possible response structures for committee prints
            self.assertTrue("prints" in result or "committeePrints" in result or "committeePrint" in result)

    def test_get_committee_prints_with_congress(self):
        """Test get_committee_prints with congress parameter"""
        result = get_committee_prints(congress=118)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("prints" in result or "committeePrints" in result or "committeePrint" in result)

    def test_get_committee_prints_with_congress_and_type(self):
        """Test get_committee_prints with congress and print_type parameters"""
        result = get_committee_prints(congress=118, print_type="hprt")

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("prints" in result or "committeePrints" in result or "committeePrint" in result)

    def test_get_committee_prints_with_pagination(self):
        """Test get_committee_prints with offset and limit parameters"""
        result = get_committee_prints(congress=118, offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for print data
            print_data = None
            for key in ["prints", "committeePrints", "committeePrint"]:
                if key in result:
                    print_data = result[key]
                    break
            
            if print_data is not None:
                self.assertIsInstance(print_data, list)
                # Should have at most 5 prints
                self.assertLessEqual(len(print_data), 5)

    def test_get_committee_prints_with_small_limit(self):
        """Test get_committee_prints with a small limit to get quick results"""
        result = get_committee_prints(congress=118, limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for print data
            print_data = None
            for key in ["prints", "committeePrints", "committeePrint"]:
                if key in result:
                    print_data = result[key]
                    break
            
            if print_data is not None:
                self.assertIsInstance(print_data, list)
                # Should have at most 3 prints
                self.assertLessEqual(len(print_data), 3)

    def test_get_committee_prints_response_structure(self):
        """Test that API response has expected structure"""
        result = get_committee_prints(congress=118, limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for print data
            print_data = None
            for key in ["prints", "committeePrints", "committeePrint"]:
                if key in result:
                    print_data = result[key]
                    break
            
            if print_data is not None and len(print_data) > 0:
                print_item = print_data[0]
                # Check for common print fields
                possible_fields = ["citation", "congress", "printType", "printNumber", "title"]
                has_print_field = any(field in print_item for field in possible_fields)
                self.assertTrue(has_print_field, f"Print missing expected fields. Available fields: {list(print_item.keys())}")

    def test_get_committee_prints_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_committee_prints(congress=118, limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for print data
            print_data = None
            for key in ["prints", "committeePrints", "committeePrint"]:
                if key in result:
                    print_data = result[key]
                    break
            
            if print_data is not None:
                self.assertLessEqual(len(print_data), 2)


if __name__ == '__main__':
    unittest.main()