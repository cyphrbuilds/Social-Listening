import requests
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config import HEADERS

@retry(stop=stop_after_attempt(3), wait=wait_exponential(), retry=retry_if_exception_type(requests.exceptions.RequestException), reraise=True)
def fetch_latest_tweets(query: str, last_seen_id: str = None) -> list:
    full_query = f"{query} since_id:{last_seen_id}" if last_seen_id else query
    logging.info(f"🚀 Searching with query: {full_query}")

    response = requests.get(
        "https://api.socialdata.tools/twitter/search",
        headers=HEADERS,
        params={"query": full_query, "type": "Latest"},
        timeout=10
    )
    response.raise_for_status()
    return response.json().get("tweets", [])
