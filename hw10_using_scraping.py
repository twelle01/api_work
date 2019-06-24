import requests
import pandas as pd
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
import datetime


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get("http://www.bbc.com", headers=headers)
doc = BeautifulSoup(response.text, 'html.parser')
MG_API_KEY = os.getenv("MAILGUN_API_KEY")

stories = doc.find_all(class_='media-list__item')
rows = []
for story in stories:
    row = {}
    headline = story.find(class_='media__link')
    if headline:
        row['headline'] = headline.text.strip()
        row['link'] = headline['href']
        try:
            row['summary'] = story.find(class_='media__summary').text.strip()
            row['channel'] = story.find(class_='media__tag').text.strip()
        except:
            pass

        rows.append(row)

df = pd.DataFrame(rows)

right_now = datetime.datetime.now()
datestring = right_now.strftime("%Y-%m-%d-%H-%M")
filename = f"briefing-{datestring}.csv"

df.to_csv(filename, index=False)

response = requests.post(
    "https://api.mailgun.net/v3/sandboxbd446712cccb4a339bc6b379efb2b0d8.mailgun.org/messages",
    auth=("api", MG_API_KEY),
    files=[("attachment", open(f"briefing-{datestring}.csv"))],
    data={"from": "Excited User <mailgun@andboxbd446712cccb4a339bc6b379efb2b0d8.mailgun.org>",
          "to": ["mht2140@columbia.edu"],
          "subject": "Here is your 6PM briefing",
          "text": "check the csv. it has great content that will blow your mind" })

response.text
