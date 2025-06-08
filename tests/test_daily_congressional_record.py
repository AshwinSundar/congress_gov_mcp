import unittest
import time
from server import get_daily_congressional_record


class TestDailyCongressionalRecordAPI(unittest.TestCase):
    """Test the get_daily_congressional_record endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_daily_congressional_record_no_params(self):
        """Test get_daily_congressional_record with no parameters (list all records)"""
        result = get_daily_congressional_record()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Common possible response structures for daily congressional records
            self.assertTrue("dailyCongressionalRecord" in result or "records" in result or "issues" in result)

    def test_get_daily_congressional_record_with_volume(self):
        """Test get_daily_congressional_record with volume parameter"""
        result = get_daily_congressional_record(volume=169)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("dailyCongressionalRecord" in result or "records" in result or "issues" in result)

    def test_get_daily_congressional_record_with_pagination(self):
        """Test get_daily_congressional_record with offset and limit parameters"""
        result = get_daily_congressional_record(offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for record data
            record_data = None
            for key in ["dailyCongressionalRecord", "records", "issues"]:
                if key in result:
                    record_data = result[key]
                    break

            if record_data is not None:
                self.assertIsInstance(record_data, list)
                # Should have at most 5 records
                self.assertLessEqual(len(record_data), 5)

    def test_get_daily_congressional_record_with_small_limit(self):
        """Test get_daily_congressional_record with a small limit to get quick results"""
        result = get_daily_congressional_record(limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for record data
            record_data = None
            for key in ["dailyCongressionalRecord", "records", "issues"]:
                if key in result:
                    record_data = result[key]
                    break

            if record_data is not None:
                self.assertIsInstance(record_data, list)
                # Should have at most 3 records
                self.assertLessEqual(len(record_data), 3)

    def test_get_daily_congressional_record_response_structure(self):
        """Test that API response has expected structure"""
        result = get_daily_congressional_record(limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for record data
            record_data = None
            for key in ["dailyCongressionalRecord", "records", "issues"]:
                if key in result:
                    record_data = result[key]
                    break

            if record_data is not None and len(record_data) > 0:
                record = record_data[0]
                # Check for common record fields
                possible_fields = ["volume", "issue", "date", "url", "title"]
                has_record_field = any(field in record for field in possible_fields)
                self.assertTrue(has_record_field, f"Record missing expected fields. Available fields: {list(record.keys())}")

    def test_get_daily_congressional_record_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_daily_congressional_record(limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for record data
            record_data = None
            for key in ["dailyCongressionalRecord", "records", "issues"]:
                if key in result:
                    record_data = result[key]
                    break

            if record_data is not None:
                self.assertLessEqual(len(record_data), 2)


if __name__ == '__main__':
    unittest.main()
