import config
import os
import requests
from datetime import datetime, timedelta

OPENAQ_API_KEY = os.environ.get('OPENAQ_API_KEY', config.OPENAQ_API_KEY)


def process(input, entities):
    # Initial variables needed for manipulations
    today_date = datetime.now().date()
    one_week_ago_date = today_date - timedelta(days=7)
    
    error_message = ""
    output_string = ""
    output = {}
    try:
        today = today_date.strftime("%Y-%m-%dT00:00:00Z")
        one_week_ago = one_week_ago_date.strftime("%Y-%m-%dT00:00:00Z")
        parameters = {}
        city = ""
        country = ""
        location_array = []

        try:
            # Check user input for city
            city = str(entities['location'][0]['value']).split(',')[0]
            # If 'city' is only two letters, it is country
            if len(city) == 2:
                country = city
            # Otherwise, it's actually city
            else:
                parameters['city'] = city
                location_array[0] = city
        except:
            pass
        # Check and get country if previous result not country
        if country == "":
            try:
                country = str(entities['location'][0]['value']).split(',')[1]
                parameters['country'] = country
                location_array[1] = country
            except:
                pass

        # URL to OpenAQ API, including country & city parameters, in that order
        url = 'https://api.openaq.org/v2/measurements?date_from=' + one_week_ago + '&date_to=' + today + '&limit=100&page=1&offset=0&radius=50'
        if country != "":
            url += '&country=' + country
        if city != "":
            url += '&city=' + city

        # Must pass None parameters if parameter dictionary is empty
        if len(parameters) == 0:
            parameters = None

        response = requests.get(url,
                                params=parameters,
                                headers={'X-API-Key': OPENAQ_API_KEY})

        # Check results and create output string (either results or error)
        output['input'] = input
        if response.status_code == 200:
            data = response.json()
            if len(data['results']) > 0:
                value = data['results'][0]['value']
                output_string = 'The AQI of ' + ','.join(location_array) + ' is ' + value
                output['output'] = output_string
            else:
                error_message = "No Results Were Found"
        elif response.status_code == 422:
            error_message = "Query Took Too Long To Find Results! Include city,country"
        else:
            error_message = "Something Went Wrong With The API Request!"
    except Exception as e:
        error_message = "There Was An Error In The Process! Reach Out To Developer!"
    finally:
        if error_message != "":
            output['error_msg'] = error_message
            output['success'] = False
        else:
            output['output'] = output_string
            output['success'] = True
    return output
