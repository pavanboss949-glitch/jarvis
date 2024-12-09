import requests
import requests_cache
from templates.text import TextTemplate

AZTRO_API_URL = "https://aztro.sameerkumar.website/"

def process(input, entities):
    output = {}
    try:
        # Extract zodiac sign and day from entities
        sign = entities.get('sign', [{}])[0].get('value', '').lower()
        day = entities.get('day', [{}])[0].get('value', 'today').lower()

        # Validate zodiac sign
        valid_signs = [
            "aries", "taurus", "gemini", "cancer", "leo", "virgo",
            "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
        ]
        if sign not in valid_signs:
            raise ValueError("Invalid zodiac sign")

        # Validate day
        valid_days = ["today", "yesterday", "tomorrow"]
        if day not in valid_days:
            raise ValueError("Invalid day")

        # Make API request
        with requests_cache.enabled('horoscope_cache', backend='sqlite', expire_after=86400):
            response = requests.post(AZTRO_API_URL, params={"sign": sign, "day": day})
            data = response.json()

        # Extract the horoscope from the response
        horoscope = data.get('description', "I couldn't fetch the horoscope right now.")

        # Create the output message
        output['input'] = input
        output['output'] = TextTemplate(f"Horoscope for {sign.capitalize()} ({day.capitalize()}):\n{horoscope}").get_message()
        output['success'] = True

    except Exception as e:
        # Error handling and fallback messages
        error_message = "I couldn't fetch your horoscope."
        error_message += "\nPlease try again with something like:"
        error_message += "\n  - horoscope for leo"
        error_message += "\n  - today's cancer horoscope"
        error_message += "\n  - tomorrow's virgo horoscope"
        output['error_msg'] = TextTemplate(error_message).get_message()
        output['success'] = False

    return output
