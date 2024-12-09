import sys
import os
import unittest

# Add the parent directory of src to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from unittest.mock import patch  # Import patch
from modules.src.horoscope import process
class TestHoroscope(unittest.TestCase):

    def test_valid_input(self): #1 
        """Test case with valid 'sign' and 'day' inputs"""
        input_text = "horoscope for aries"
        entities = {"sign": [{"value": "aries"}], "day": [{"value": "today"}]}
        result = process(input_text, entities)
        self.assertIn("output", result)
        self.assertTrue(result["success"])

    def test_missing_day(self): #2
        """Test case with 'sign' provided but missing 'day'"""
        input_text = "horoscope for aries"
        entities = {"sign": [{"value": "aries"}]}
        result = process(input_text, entities)
        self.assertIn("output", result)
        self.assertTrue(result["success"])

    def test_missing_sign(self):#3
        """Test case with 'day' provided but missing 'sign'"""
        input_text = "horoscope for today"
        entities = {"day": [{"value": "today"}]}
        result = process(input_text, entities)
        self.assertIn("error_msg", result)
        self.assertFalse(result["success"])

    def test_invalid_sign(self):#4
        """Test case with an invalid zodiac sign"""
        input_text = "horoscope for dragon"
        entities = {"sign": [{"value": "dragon"}], "day": [{"value": "today"}]}
        result = process(input_text, entities)
        self.assertIn("error_msg", result)
        self.assertFalse(result["success"])

    def test_invalid_day(self):#5
        """Test case with an invalid day"""
        input_text = "horoscope for aries on someday"
        entities = {"sign": [{"value": "aries"}], "day": [{"value": "someday"}]}
        result = process(input_text, entities)
        self.assertIn("error_msg", result)
        self.assertFalse(result["success"])


    def test_all_zodiac_signs(self):#7
        """Test with all valid zodiac signs"""
        zodiac_signs = [
            "aries", "taurus", "gemini", "cancer", "leo", "virgo",
            "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
        ]
        for sign in zodiac_signs:
            with self.subTest(sign=sign):

                input_text = f"horoscope for {sign}"
                entities = {"sign": [{"value": sign}], "day": [{"value": "today"}]}
                result = process(input_text, entities)
                self.assertIn("output", result)
                self.assertTrue(result["success"])
    def test_all_days(self):#8
        """Test with all valid day inputs"""
        days = ["yesterday", "today", "tomorrow"]
        for day in days:
            with self.subTest(day=day):
                input_text = f"horoscope for aries on {day}"
                entities = {"sign": [{"value": "aries"}], "day": [{"value": day}]}
                result = process(input_text, entities)
                self.assertIn("output", result)
                self.assertTrue(result["success"])
    def test_fuzzy_inputs(self):  # Include this inside the TestHoroscope class
        """Test fuzzy inputs for zodiac signs"""
        fuzzy_inputs = ["aeries", "taurrus", "jimini", "leo.", "cancer@", "sagitarius"]
        for fuzzy_sign in fuzzy_inputs:
            with self.subTest(fuzzy_sign=fuzzy_sign):
                input_text = f"horoscope for {fuzzy_sign}"
                entities = {"sign": [{"value": fuzzy_sign}], "day": [{"value": "today"}]}
                result = process(input_text, entities)
                self.assertIn("error_msg", result)
                self.assertFalse(result["success"])

    def test_empty_entities(self):  # Include this inside the TestHoroscope class
        """Test behavior with empty entities"""
        input_text = "horoscope"
        entities = {}
        result = process(input_text, entities)
        self.assertIn("error_msg", result)
        self.assertFalse(result["success"])

    def test_completely_invalid_input(self):
        """Test with a completely invalid input"""
        input_text = "random gibberish"
        entities = {}
        result = process(input_text, entities)
        self.assertIn("error_msg", result)
        self.assertFalse(result["success"])
    def test_edge_case_inputs(self): # fails
        """Test edge cases for input text and entities"""
        edge_cases = [
            {"input_text": "", "entities": {"sign": [{"value": "aries"}], "day": [{"value": "today"}]}},
            {"input_text": "123456", "entities": {"sign": [{"value": "123456"}], "day": [{"value": "today"}]}},
            {"input_text": "!@#$%^&*", "entities": {"sign": [{"value": "!@#$%^&*"}], "day": [{"value": "today"}]}},
        ]
        for case in edge_cases:
            with self.subTest(input_text=case["input_text"]):
                result = process(case["input_text"], case["entities"])
                self.assertIn("error_msg", result)
                self.assertFalse(result["success"])
    @patch("modules.src.horoscope.requests.get")
    def test_api_unavailability(self, mock_get):
        """Test behavior when the API is unavailable"""
        mock_get.side_effect = requests.exceptions.ConnectionError
        input_text = "horoscope for aries today"
        entities = {"sign": [{"value": "aries"}], "day": [{"value": "today"}]}
        result = process(input_text, entities)
        self.assertIn("error_msg", result)
        self.assertFalse(result["success"])
    @patch("modules.src.horoscope.requests.get")
    def test_api_timeout(self, mock_get):
        """Test behavior when the API times out"""
        mock_get.side_effect = requests.exceptions.Timeout
        input_text = "horoscope for leo today"
        entities = {"sign": [{"value": "leo"}], "day": [{"value": "today"}]}
        result = process(input_text, entities)
        self.assertIn("error_msg", result)
        self.assertFalse(result["success"])
    @patch("modules.src.horoscope.requests.get")
    def test_malformed_api_response(self, mock_get):
        """Test behavior with a malformed API response"""
        mock_get.return_value.json.return_value = {"unexpected": "data"}
        input_text = "horoscope for cancer today"
        entities = {"sign": [{"value": "cancer"}], "day": [{"value": "today"}]}
        result = process(input_text, entities)
        self.assertIn("error_msg", result)
        self.assertFalse(result["success"])

if __name__ == "__main__":
    unittest.main()

