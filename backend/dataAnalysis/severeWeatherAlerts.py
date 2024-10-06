import requests
from opencage.geocoder import OpenCageGeocode

# US ONLY
def get_severe_weather_alerts(latitude, longitude):
    opencage_api_key = 'bb679099bd004c7ab8d5dfe4dec28281'
    geocoder = OpenCageGeocode(opencage_api_key)

    alert_message = "No severe weather alerts found."

    result = geocoder.reverse_geocode(latitude, longitude)
    if result and len(result):
        address = result[0]['components']

        country = address.get('country', '')

        if country == 'United States':
            state = address.get('state_code', '')

            url = f"https://api.weather.gov/alerts/active?area={state}"
            response = requests.get(url)

            data = response.json()

            if data['features']:
                properties = data['features'][0]['properties']['parameters']
                nws_headline = properties.get('NWSheadline', 'No headline')
                alert_message = "There are severe weather alerts in your area. Please take caution. Alert: " + \
                    str(nws_headline[0])
            else:
                alert_message = "There are no severe weather alerts in your area."
        else:
            alert_message = "Severe weather alerts are only available for the United States."
    else:
        print("No address found for the given coordinates.")

    return alert_message
                    