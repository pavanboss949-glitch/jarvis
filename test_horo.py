from modules.src.horoscope import process
import unittest

# Direct tests
# -----------------
# Test case 1: Valid input
input_text = "Tell me the horoscope for Aries today"
entities = {
    "sign": [{"value": "aries"}],
    "day": [{"value": "today"}]
}

# Test case 2: Missing 'day'
input_text_missing_day = "Tell me the horoscope for Aries"
entities_missing_day = {
    "sign": [{"value": "aries"}]
}

# Test case 3: Missing 'sign'
input_text_missing_sign = "Tell me the horoscope for today"
entities_missing_sign = {
    "day": [{"value": "today"}]
}

# Running direct tests
print("Test 1: Valid input")
print(process(input_text, entities))

print("\nTest 2: Missing 'day'")
print(process(input_text_missing_day, entities_missing_day))

print("\nTest 3: Missing 'sign'")
print(process(input_text_missing_sign, entities_missing_sign))

# Unit test class
# -----------------
class TestHoroscope(unittest.TestCase):
    def test_horoscope(self):   
        input_text = "horoscope for aries"
        entities = {"sign": [{"value": "aries"}], "day": [{"value": 
"today"}]}
        result = process(input_text, entities)
        self.assertIn("output", result)
        self.assertTrue(result["success"])

if __name__ == "__main__":
    unittest.main()

