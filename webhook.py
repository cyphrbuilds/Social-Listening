import requests
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config import WEBHOOK_URL

@retry(stop=stop_after_attempt(3), wait=wait_exponential(), retry=retry_if_exception_type(requests.exceptions.RequestException), reraise=True)
def send_webhook(tweet_data: dict):
    response = requests.post(WEBHOOK_URL, json=tweet_data, timeout=10)
    response.raise_for_status()
    logging.info(f"Webhook sent for tweet ID {tweet_data['id']}")
