import json
import os
import hashlib
from config import STATE_FILE, TWEET_ARCHIVE_FILE

def get_query_key(query: str) -> str:
    return hashlib.sha256(query.encode()).hexdigest()

def load_last_seen_id(query: str) -> str | None:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return data.get(get_query_key(query))
    return None

def save_last_seen_id(query: str, tweet_id: str):
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    state[get_query_key(query)] = tweet_id
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def load_tweet_archive() -> list:
    if os.path.exists(TWEET_ARCHIVE_FILE):
        with open(TWEET_ARCHIVE_FILE, "r") as f:
            return json.load(f)
    return []

def save_tweet_archive(tweets: list):
    with open(TWEET_ARCHIVE_FILE, "w") as f:
        json.dump(tweets, f, indent=2)
