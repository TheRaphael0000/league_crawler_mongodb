import sys
import random
import os
from dotenv import load_dotenv
import pymongo
from .api import api_request
from datetime import datetime

load_dotenv()


mongo_connection = {
    "host": os.getenv("MONGO_HOST"),
    "port": int(os.getenv("MONGO_PORT")),
    "username": os.getenv("MONGO_USERNAME"),
    "password": os.getenv("MONGO_PASSWORD"),
}

client = pymongo.MongoClient(**mongo_connection)
db = client.league
matches = db.matches
puuid_visited = db.puuid_visited

match_count = 5
match_queue = 420  # 5v5 solo queue
server = "EUW1"


def get_random_puuid():
    pipeline = [
        {"$sample": {"size": 1}},
        {"$project": {"_id": 0, "participants": "$metadata.participants"}},
    ]
    result = list(matches.aggregate(pipeline))
    participants = result[0]["participants"]
    puuid = random.choice(participants)
    return puuid


limited = True  # limited mod to avoid puuid exhaustion

try:
    while True:
        # try to use a random root from the current db
        try:
            puuid = get_random_puuid()
        except:
            # neeko tesla # euw
            puuid = "WxfttxnFvXNai1rAR08Ph8qAE0d5ZQyNPkErp6MPqXABJfZRzCh8j5tzGKWifdmkglCTGp--eNYhHA"

        if puuid_visited.find_one({"_id": puuid}):
            continue

        if limited:
            limited = matches.count_documents({}) < 5

        try:
            matches_id = api_request(
                f"/lol/match/v5/matches/by-puuid/{puuid}/ids?count={match_count}&queue={match_queue}")
            try:
                puuid_visited.insert_one({"_id": puuid})
            except:
                pass

        except Exception as e:
            print(datetime.now().isoformat(), e, file=sys.stderr)
            continue

        for match_id in matches_id:

            in_db = matches.count_documents({"_id": match_id}) >= 1

            if in_db and not limited:
                continue

            try:
                match = api_request(f"/lol/match/v5/matches/{match_id}")
                match["_id"] = match["metadata"]["matchId"]

                if in_db:
                    continue

                matches.insert_one(match)

            except Exception as e:
                print(datetime.now().isoformat(), e, file=sys.stderr)
                continue

except KeyboardInterrupt as e:
    print(datetime.now().isoformat(), e, file=sys.stderr)
