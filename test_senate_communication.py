import unittest
import time
from server import get_senate_communication


class TestSenateCommunicationAPI(unittest.TestCase):
    """Test the get_senate_communication endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_senate_communication_no_params(self):
        """Test get_senate_communication with no parameters (list all communications)"""
        result = get_senate_communication()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Common possible response structures for senate communications
            self.assertTrue("senateCommunications" in result or "communications" in result or "senateCommunication" in result)

    def test_get_senate_communication_with_congress(self):
        """Test get_senate_communication with congress parameter"""
        result = get_senate_communication(congress=118)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("senateCommunications" in result or "communications" in result or "senateCommunication" in result)

    def test_get_senate_communication_with_congress_and_type(self):
        """Test get_senate_communication with congress and communication_type parameters"""
        result = get_senate_communication(congress=118, communication_type="ec")

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertTrue("senateCommunications" in result or "communications" in result or "senateCommunication" in result)

    def test_get_senate_communication_with_pagination(self):
        """Test get_senate_communication with offset and limit parameters"""
        result = get_senate_communication(congress=118, offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for communication data
            comm_data = None
            for key in ["senateCommunications", "communications", "senateCommunication"]:
                if key in result:
                    comm_data = result[key]
                    break
            
            if comm_data is not None:
                self.assertIsInstance(comm_data, list)
                # Should have at most 5 communications
                self.assertLessEqual(len(comm_data), 5)

    def test_get_senate_communication_with_small_limit(self):
        """Test get_senate_communication with a small limit to get quick results"""
        result = get_senate_communication(congress=118, limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for communication data
            comm_data = None
            for key in ["senateCommunications", "communications", "senateCommunication"]:
                if key in result:
                    comm_data = result[key]
                    break
            
            if comm_data is not None:
                self.assertIsInstance(comm_data, list)
                # Should have at most 3 communications
                self.assertLessEqual(len(comm_data), 3)

    def test_get_senate_communication_response_structure(self):
        """Test that API response has expected structure"""
        result = get_senate_communication(congress=118, limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for communication data
            comm_data = None
            for key in ["senateCommunications", "communications", "senateCommunication"]:
                if key in result:
                    comm_data = result[key]
                    break
            
            if comm_data is not None and len(comm_data) > 0:
                communication = comm_data[0]
                # Check for common communication fields
                possible_fields = ["congress", "type", "number", "communicationType"]
                has_comm_field = any(field in communication for field in possible_fields)
                self.assertTrue(has_comm_field, f"Communication missing expected fields. Available fields: {list(communication.keys())}")

    def test_get_senate_communication_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_senate_communication(congress=118, limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            # Check for communication data
            comm_data = None
            for key in ["senateCommunications", "communications", "senateCommunication"]:
                if key in result:
                    comm_data = result[key]
                    break
            
            if comm_data is not None:
                self.assertLessEqual(len(comm_data), 2)


if __name__ == '__main__':
    unittest.main()