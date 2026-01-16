import requests
import os
from dotenv import load_dotenv
import time
from datetime import datetime

load_dotenv()

riot_endpoint = "https://europe.api.riotgames.com"
league_endpoint = "https://{0}.api.riotgames.com"
sleep_time = 115

def api_request(url, region=None):
    if region is None:
        url = f"{riot_endpoint}{url}"
    else:
        url = f"{league_endpoint.format(region)}{url}"

    print(datetime.now().isoformat(), url)

    while True:
        response = requests.get(url, headers={"X-Riot-Token": os.getenv("RIOT_API_KEY")})
        
        print(datetime.now().isoformat(), response.status_code)
        data = response.json()
        code = response.status_code

        if code == 429 or str(code)[0] == '5':
            print(datetime.now().isoformat(), f"Sleep {sleep_time} ({code})")
            time.sleep(sleep_time)
        elif str(code)[0] == '4':
            print(datetime.now().isoformat(), f"Probably invalid configuration")
            exit()
        elif code != 200:
            raise Exception(f"error {code}")
        else:
            return data