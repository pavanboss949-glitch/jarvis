import requests

API_URL = "https://words.bighugelabs.com/api/2"

def process(input_text, entities):
    output = {}
    try:
        word = entities["word"][0]["value"]
        api_key = "hardcoded_api_key"# Its best practice not to store api key directly in the code
        # The code assumes that word is always present in entities missing input will cause a crash.

        response = requests.get(f"{API_URL}/{api_key}/{word}/json")
        data = response.json()  

        synonyms = data["noun"]["syn"]
        #The api lets you do mort parts of speech than just a noun 
        output["output"] = f"Synonyms: {', '.join(synonyms)}"
        output["success"] = True
# code assumes the API request will always succeed, but it may fail due to network issues, invalid API keys, or server errors.

    except:
        output["error_msg"] = "An error occurred."
        output["success"] = False
    # error reports are too vague and needs to be more in depth for best practice and makes error hndling simpler
    return output

