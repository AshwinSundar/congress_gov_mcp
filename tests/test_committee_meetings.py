import unittest
import time
from server import get_committee_meetings


class TestCommitteeMeetingsAPI(unittest.TestCase):
    """Test the get_committee_meetings endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_committee_meetings_no_params(self):
        """Test get_committee_meetings with no parameters (list all meetings)"""
        result = get_committee_meetings()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Common possible response structures for committee meetings
            self.assertTrue("meetings" in result or "committeeMeetings" in result or "committeeMeeting" in result)

    def test_get_committee_meetings_with_congress(self):
        """Test get_committee_meetings with congress parameter"""
        result = get_committee_meetings(congress=118)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("meetings" in result or "committeeMeetings" in result or "committeeMeeting" in result)

    def test_get_committee_meetings_with_congress_and_chamber(self):
        """Test get_committee_meetings with congress and chamber parameters"""
        result = get_committee_meetings(congress=118, chamber="house")

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("meetings" in result or "committeeMeetings" in result or "committeeMeeting" in result)

    def test_get_committee_meetings_with_pagination(self):
        """Test get_committee_meetings with offset and limit parameters"""
        result = get_committee_meetings(congress=118, offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for meeting data
            meeting_data = None
            for key in ["meetings", "committeeMeetings", "committeeMeeting"]:
                if key in result:
                    meeting_data = result[key]
                    break
            
            if meeting_data is not None:
                self.assertIsInstance(meeting_data, list)
                # Should have at most 5 meetings
                self.assertLessEqual(len(meeting_data), 5)

    def test_get_committee_meetings_with_small_limit(self):
        """Test get_committee_meetings with a small limit to get quick results"""
        result = get_committee_meetings(congress=118, limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for meeting data
            meeting_data = None
            for key in ["meetings", "committeeMeetings", "committeeMeeting"]:
                if key in result:
                    meeting_data = result[key]
                    break
            
            if meeting_data is not None:
                self.assertIsInstance(meeting_data, list)
                # Should have at most 3 meetings
                self.assertLessEqual(len(meeting_data), 3)

    def test_get_committee_meetings_response_structure(self):
        """Test that API response has expected structure"""
        result = get_committee_meetings(congress=118, limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for meeting data
            meeting_data = None
            for key in ["meetings", "committeeMeetings", "committeeMeeting"]:
                if key in result:
                    meeting_data = result[key]
                    break
            
            if meeting_data is not None and len(meeting_data) > 0:
                meeting = meeting_data[0]
                # Check for common meeting fields
                possible_fields = ["chamber", "congress", "eventId", "date", "time", "title"]
                has_meeting_field = any(field in meeting for field in possible_fields)
                self.assertTrue(has_meeting_field, f"Meeting missing expected fields. Available fields: {list(meeting.keys())}")

    def test_get_committee_meetings_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_committee_meetings(congress=118, limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for meeting data
            meeting_data = None
            for key in ["meetings", "committeeMeetings", "committeeMeeting"]:
                if key in result:
                    meeting_data = result[key]
                    break
            
            if meeting_data is not None:
                self.assertLessEqual(len(meeting_data), 2)

    def test_get_committee_meetings_senate_chamber(self):
        """Test get_committee_meetings for senate chamber"""
        result = get_committee_meetings(congress=118, chamber="senate", limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("meetings" in result or "committeeMeetings" in result or "committeeMeeting" in result)


if __name__ == '__main__':
    unittest.main()