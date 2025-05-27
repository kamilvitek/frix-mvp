# Zavolat endpointy Eventbrite API, např. /events/search, s parametry jako město nebo časové období.
# Zpracovat odpověď (JSON) – vyzobat z každé události nejdůležitější pole:
# id
# name.text (název)
# start.local a end.local (datum/čas)
# venue_id (místo konání)
# případně category/tags
# Tyto údaje vrátit z funkce importeru jako seznam Python slovníků nebo jako instanci třídy (viz níže).

import os
from dotenv import load_dotenv
import requests

###Import .env
load_dotenv(os.getenv(".env"))  # print(os.getenv("EVENTBRITE_PRIVATE_TOKEN"))

client_id = os.getenv("EVENTBRITE_API")
client_secret = os.getenv("EVENTBRITE_CLIENT_SECRET")
redirect_uri = "http://localhost:3000/api/auth/callback"
url = (
    "https://www.eventbrite.com/oauth/authorize"
    "?response_type=code"
    f"&client_id={client_id}"
    f"&redirect_uri={redirect_uri}"
)

code = "XN2KFUXCC6DXWJBY7UBW"

###Variables above saved into one variable "data"
data = {
  "client_id": client_id,
  "client_secret": client_secret,
  "redirect_uri": redirect_uri,
  "code": code,
  "grant_type": "authorization_code"
}

###Getting access token. Context here: "https://www.eventbrite.com/platform/api#/introduction/authentication/2.-(for-app-partners)-authorize-your-users"
resp = requests.post("https://www.eventbrite.com/oauth/token",
                     data=data,
                     headers={"content-type": "application/x-www-form-urlencoded"})
# print("STATUS:", resp.status_code)
# print("BODY  :", resp.text)
# resp.raise_for_status()
# token_json = resp.json()
# print("ACCESS_TOKEN:", token_json["access_token"])

###Saving acces_token
access_token = "IZAVO66PKDGLMNJWXPLY"

###Preparing "headers" for the next requests
headers = {
  "Authorization": f"Bearer {access_token}"
}

###API function test
# resp = requests.get(
#     "https://www.eventbriteapi.com/v3/users/me/",
#     headers=headers
# )
# print("→ GET /users/me/ status:", resp.status_code)
# print("→ GET /users/me/ body:", resp.json())

