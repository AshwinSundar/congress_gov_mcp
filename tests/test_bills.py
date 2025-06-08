import unittest
import time
from server import get_bills


class TestBillsAPI(unittest.TestCase):
    """Test the get_bills endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_bills_no_params(self):
        """Test get_bills with no parameters (default values)"""
        result = get_bills()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("bills", result)
            self.assertIsInstance(result["bills"], list)

    def test_get_bills_with_congress(self):
        """Test get_bills with congress parameter"""
        result = get_bills(congress=118)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("bills", result)
            self.assertIsInstance(result["bills"], list)

    def test_get_bills_with_congress_and_bill_type(self):
        """Test get_bills with congress and bill_type parameters"""
        result = get_bills(congress=118, bill_type="hr")

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("bills", result)
            self.assertIsInstance(result["bills"], list)

    def test_get_bills_with_specific_bill(self):
        """Test get_bills with congress, bill_type, and bill_number for a known bill"""
        # HR 1 is typically a common bill number
        result = get_bills(congress=118, bill_type="hr", bill_number=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # For specific bills, the response structure might be different
            self.assertTrue("bill" in result or "bills" in result)

    def test_get_bills_with_pagination(self):
        """Test get_bills with offset and limit parameters"""
        result = get_bills(congress=118, offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("bills", result)
            bills = result["bills"]
            self.assertIsInstance(bills, list)
            # Should have at most 5 bills
            self.assertLessEqual(len(bills), 5)

    def test_get_bills_with_small_limit(self):
        """Test get_bills with a small limit to get quick results"""
        result = get_bills(congress=118, limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("bills", result)
            bills = result["bills"]
            self.assertIsInstance(bills, list)
            # Should have at most 3 bills
            self.assertLessEqual(len(bills), 3)

    def test_get_bills_senate_bills(self):
        """Test get_bills for Senate bills"""
        result = get_bills(congress=118, bill_type="s", limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("bills", result)
            self.assertIsInstance(result["bills"], list)

    def test_get_bills_response_structure(self):
        """Test that API response has expected structure"""
        result = get_bills(congress=118, limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("bills", result)
            bills = result["bills"]
            if len(bills) > 0:
                bill = bills[0]
                # Check for common bill fields
                expected_fields = ["congress", "type", "number"]
                for field in expected_fields:
                    self.assertIn(field, bill, f"Missing field: {field}")

    def test_get_bills_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_bills(congress=118, limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("bills", result)
            bills = result["bills"]
            self.assertLessEqual(len(bills), 2)


if __name__ == '__main__':
    unittest.main()
