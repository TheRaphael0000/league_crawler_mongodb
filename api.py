import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

riot_endpoint = "https://europe.api.riotgames.com"
league_endpoint = "https://{0}.api.riotgames.com"

def api_request(url, region=None):
    if region is None:
        url = f"{riot_endpoint}{url}"
    else:
        url = f"{league_endpoint.format(region)}{url}"

    print(url, end=" ")

    while True:
        response = requests.get(url, headers={"X-Riot-Token": os.getenv("RIOT_API_KEY")})
        
        print(response.status_code)
        data = response.json()

        if response.status_code == 429:
            print("Sleep", 115)
            time.sleep(115)
        elif str(response.status_code)[0] == '4':
            exit()
        elif response.status_code != 200:
            raise Exception(f"error {response.status_code}")
        else:
            return data