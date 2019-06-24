import requests
import os
from dotenv import load_dotenv
load_dotenv()
import datetime

API_KEY = os.getenv("DARKSKY_API_KEY")
MG_API_KEY = os.getenv("MAILGUN_API_KEY")

NY = ("40,-78") #NYC
response = requests.get(f'https://api.darksky.net/forecast/{API_KEY}/{NY}?units=si')
sky_ny = response.json()

right_now = datetime.datetime.now()
date_string = right_now.strftime("%B %d, %Y")

warm = 19
current = sky_ny['currently']
daily = sky_ny['daily']['data'][0]

if current['apparentTemperature'] > warm:
    text_i = (f'Right now it is {current["temperature"]} degrees out and {current["summary"]}. Today it will be warm with a high of {daily["temperatureHigh"]} and a low of {daily["temperatureMin"]}')
else:
    text_i = (f'Right now it is {current["temperature"]} degrees out and {current["summary"]}. Today it will be cold with a high of {daily["temperatureHigh"]} and a low of {daily["temperatureMin"]}')

response = requests.post(
    "https://api.mailgun.net/v3/sandboxbd446712cccb4a339bc6b379efb2b0d8.mailgun.org/messages",
    auth=("api", MG_API_KEY),
    data={"from": "Excited User <mailgun@andboxbd446712cccb4a339bc6b379efb2b0d8.mailgun.org>",
          "to": ["mht2140@columbia.edu"],
          "subject": "8 AM Weather forecast:"+ date_string,
          "text": text_i })


response.text