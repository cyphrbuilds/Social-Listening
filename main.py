import time
import logging
import schedule
from config import LOG_FILE, TWITTER_SEARCH_QUERY
from fetcher import fetch_latest_tweets
from webhook import send_webhook
from storage import load_last_seen_id, save_last_seen_id, load_tweet_archive, save_tweet_archive

# === LOGGING ===
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def check_for_new_tweets(query: str):
    logging.info("Checking for new tweets...")
    last_seen_id = load_last_seen_id(query)
    tweets = fetch_latest_tweets(query, last_seen_id)

    if not tweets:
        logging.info("No tweets found.")
        return

    tweets.sort(key=lambda x: int(x["id"]))
    logging.info(f"Found {len(tweets)} new tweet(s)")

    archive = load_tweet_archive()
    archive += tweets
    save_tweet_archive(archive)
    logging.info(f"📦 Archived {len(tweets)} new tweet(s)")

    for tweet in tweets:
        send_webhook(tweet)

    save_last_seen_id(query, tweets[-1]["id"])

# === SCHEDULE ===
schedule.every(1).minutes.do(lambda: check_for_new_tweets(TWITTER_SEARCH_QUERY))

logging.info("Twitter Listener started...")
check_for_new_tweets(TWITTER_SEARCH_QUERY)

while True:
    schedule.run_pending()
    time.sleep(1)
