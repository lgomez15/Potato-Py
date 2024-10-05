import requests

latitude = 39.7456   
longitude = -97.7431

url = f"https://api.weather.gov/points/{latitude},{longitude}"
response = requests.get(url)
                       
print(response.json())