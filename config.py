import os
from dotenv import load_dotenv

load_dotenv()
SOCIALDATA_API_KEY = os.getenv("SOCIALDATA_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

TWITTER_SEARCH_QUERY = "list:1909301727892779438 -filter:replies -filter:nativeretweets -filter:quote"
STATE_FILE = "last_seen.json"
TWEET_ARCHIVE_FILE = "tweets.json"
LOG_FILE = "listener.log"

HEADERS = {"Authorization": f"Bearer {SOCIALDATA_API_KEY}"}