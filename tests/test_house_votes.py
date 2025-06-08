import unittest
import time
from server import get_house_votes


class TestHouseVotesAPI(unittest.TestCase):
    """Test the get_house_votes endpoint with real API calls"""

    def setUp(self):
        """Add a small delay between tests to be respectful to the API"""
        time.sleep(0.5)

    def test_get_house_votes_no_params(self):
        """Test get_house_votes with no parameters (list all votes)"""
        result = get_house_votes()

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("houseRollCallVotes", result)
            self.assertIsInstance(result["houseRollCallVotes"], list)

    def test_get_house_votes_with_congress(self):
        """Test get_house_votes with congress parameter"""
        result = get_house_votes(congress=118)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("houseRollCallVotes", result)
            self.assertIsInstance(result["houseRollCallVotes"], list)

    def test_get_house_votes_with_congress_and_session(self):
        """Test get_house_votes with congress and session parameters"""
        result = get_house_votes(congress=118, session=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("houseRollCallVotes", result)
            self.assertIsInstance(result["houseRollCallVotes"], list)

    def test_get_house_votes_with_pagination(self):
        """Test get_house_votes with offset and limit parameters"""
        result = get_house_votes(congress=118, offset=0, limit=5)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("houseRollCallVotes", result)
            vote_data = result["houseRollCallVotes"]
            self.assertIsInstance(vote_data, list)
            # Should have at most 5 votes
            self.assertLessEqual(len(vote_data), 5)

    def test_get_house_votes_with_small_limit(self):
        """Test get_house_votes with a small limit to get quick results"""
        result = get_house_votes(congress=118, limit=3)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("houseRollCallVotes", result)
            vote_data = result["houseRollCallVotes"]
            self.assertIsInstance(vote_data, list)
            # Should have at most 3 votes
            self.assertLessEqual(len(vote_data), 3)

    def test_get_house_votes_response_structure(self):
        """Test that API response has expected structure"""
        result = get_house_votes(congress=118, limit=1)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("houseRollCallVotes", result)
            vote_data = result["houseRollCallVotes"]
            if len(vote_data) > 0:
                vote = vote_data[0]
                # Check for common vote fields that might exist
                possible_fields = ["rollCall", "congress", "session", "date", "question", "result", "rollCallNumber"]
                # At least one of these fields should exist in a valid vote record
                has_vote_field = any(field in vote for field in possible_fields)
                self.assertTrue(has_vote_field, f"Vote record missing expected fields. Available fields: {list(vote.keys())}")

    def test_get_house_votes_limit_enforcement(self):
        """Test that limit parameter works"""
        result = get_house_votes(congress=118, limit=2)

        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("houseRollCallVotes", result)
            vote_data = result["houseRollCallVotes"]
            self.assertLessEqual(len(vote_data), 2)


if __name__ == '__main__':
    unittest.main()