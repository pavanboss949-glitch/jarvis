import requests
import config
from templates.text import TextTemplate

API_URL = "https://words.bighugelabs.com/api/2"

def process(input_text, entities):
    output = {}
    try:
        # Extract the word from the entities
        word = entities.get("word", [{}])[0].get("value", "")
        if not word.strip():
            raise ValueError("Input cannot be empty. Please provide a valid word for thesaurus lookup.")

        # Make the API request
        response = requests.get(f"{API_URL}/{config.BHT_THESAURUS_API_KEY}/{word}/json")
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")

        # Parse the JSON response
        try:
            data = response.json()
        except ValueError:
            raise ValueError("Malformed API response. Please try again later.")

        # Extract synonyms from the response
        synonyms = []
        for key in ["noun", "verb", "adjective", "adverb"]:
            if key in data and "syn" in data[key]:
                synonyms.extend(data[key]["syn"])

        if synonyms:
            output_text = f"Synonyms for '{word}':\n" + ", ".join(synonyms)
            output["output"] = TextTemplate(output_text).get_message()
            output["success"] = True
        else:
            output["error_msg"] = TextTemplate(f"Couldn't find synonyms for '{word}'.").get_message()
            output["success"] = False
    except Exception as e:
        output["error_msg"] = TextTemplate(f"An error occurred: {str(e)}").get_message()
        output["success"] = False

    return output
