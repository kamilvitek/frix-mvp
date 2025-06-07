import os
from dotenv import load_dotenv
import requests


#import .env
load_dotenv(os.getenv(".env"))  # print(os.getenv("PREDICT_HQ_API"))
predict_hq = os.getenv("PREDICT_HQ_API")


###You can find more info on:
#   https://control.predicthq.com/explorer/events
#   https://docs.predicthq.com/getting-started/api-quickstart
response = requests.get(
  url="https://api.predicthq.com/v1/events",
  headers={
    "Authorization": f"Bearer {predict_hq}",
    "Accept": "application/json"
  },
  params={
   "country": "CZ"
  }
)

print(response.json())