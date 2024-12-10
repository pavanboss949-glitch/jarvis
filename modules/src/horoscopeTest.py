import requests

AZTRO_API_URL = "https://aztro.sameerkumar.website/"

def process(input, entities):
    output = {}
    try:
        sign = ""
        if "sign" in entities and len(entities["sign"]) > 0:
            sign = entities["sign"][0]["value"].lower()
        day = "today" # if you extract the specific day and value from the entities would make the code concise and readable
        if "day" in entities and len(entities["day"]) > 0:
            day = entities["day"][0]["value"].lower()
        #Add checks for valid zodiac signs and days,
        # the code needs to ensure the input aligns with lists of valid values for both days and signs
        response = requests.post(AZTRO_API_URL, params={"sign": sign, "day": day})
        if response.status_code != 200:
            raise Exception("API request failed")

        data = response.json()
        horoscope = data["description"] if "description" in data else "Horoscope not available."
        # needs to have handling for when api returns empty results 
        output["input"] = input
        output["output"] = {"text": f"Horoscope for {sign.capitalize()} ({day.capitalize()}): {horoscope}"}
        output["success"] = True

    except Exception as e:
        output["error_msg"] = {"text": "An error occurred. Try again later."}
        output["success"] = False
#Error messages needs to be less vague for good practice
        return output

