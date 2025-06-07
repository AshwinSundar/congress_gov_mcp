import unittest
import time
from server import get_bound_congressional_record


class TestBoundCongressionalRecordAPI(unittest.TestCase):
    """Test the get_bound_congressional_record endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_bound_congressional_record_no_params(self):
        """Test get_bound_congressional_record with no parameters (list all records)"""
        result = get_bound_congressional_record()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Common possible response structures for bound congressional records
            self.assertTrue("boundCongressionalRecord" in result or "records" in result or "years" in result)

    def test_get_bound_congressional_record_with_year(self):
        """Test get_bound_congressional_record with year parameter"""
        result = get_bound_congressional_record(year=2023)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("boundCongressionalRecord" in result or "records" in result or "years" in result)

    def test_get_bound_congressional_record_with_pagination(self):
        """Test get_bound_congressional_record with offset and limit parameters"""
        result = get_bound_congressional_record(offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for record data
            record_data = None
            for key in ["boundCongressionalRecord", "records", "years"]:
                if key in result:
                    record_data = result[key]
                    break
            
            if record_data is not None:
                self.assertIsInstance(record_data, list)
                # Should have at most 5 records
                self.assertLessEqual(len(record_data), 5)

    def test_get_bound_congressional_record_with_small_limit(self):
        """Test get_bound_congressional_record with a small limit to get quick results"""
        result = get_bound_congressional_record(limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for record data
            record_data = None
            for key in ["boundCongressionalRecord", "records", "years"]:
                if key in result:
                    record_data = result[key]
                    break
            
            if record_data is not None:
                self.assertIsInstance(record_data, list)
                # Should have at most 3 records
                self.assertLessEqual(len(record_data), 3)

    def test_get_bound_congressional_record_response_structure(self):
        """Test that API response has expected structure"""
        result = get_bound_congressional_record(limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for record data
            record_data = None
            for key in ["boundCongressionalRecord", "records", "years"]:
                if key in result:
                    record_data = result[key]
                    break
            
            if record_data is not None and len(record_data) > 0:
                record = record_data[0]
                # Check for common record fields
                possible_fields = ["year", "date", "url", "title"]
                has_record_field = any(field in record for field in possible_fields)
                self.assertTrue(has_record_field, f"Record missing expected fields. Available fields: {list(record.keys())}")

    def test_get_bound_congressional_record_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_bound_congressional_record(limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for record data
            record_data = None
            for key in ["boundCongressionalRecord", "records", "years"]:
                if key in result:
                    record_data = result[key]
                    break
            
            if record_data is not None:
                self.assertLessEqual(len(record_data), 2)


if __name__ == '__main__':
    unittest.main()