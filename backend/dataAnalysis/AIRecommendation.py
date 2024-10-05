from openai import OpenAI
from datetime import datetime

client = OpenAI()
air_temp = 25
land_temp = 28
humidity = 54
wind_speed = 10
rain_24h = 2
current_date = datetime.now().strftime("%Y-%m-%d")
location = "Salamanca, Spain"

possible_plants = ["tomato", "corn", "wheat", "potato", "sunflower", "soybean", \
                   "cotton", "sugarcane", "rice", "barley", "yam", "oranges", "grapes", \
                    "onions", "peanuts", "cabbage", "carrots", "lettuce", "peppers", "pumpkin", \
                    "sweet potatoes", "watermelon", "apples", "bananas", "mangoes", "pineapples", \
                    "bananas", "avocado"]

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"The current air temperature is {air_temp} degrees Celsius. /
            The current land temperature is {land_temp} degrees Celsius. /
            The current humidity is {humidity}%. /
            The current wind speed is {wind_speed} km/h. /
            The rainfall in the last 24 hours is {rain_24h} mm. /
            Today's date is {current_date}. /
            I am located in {location}. /
            In one word can you provide the best crop to plant today out of {possible_plants}?"
        }
    ]
)

print(completion.choices[0].message)
