import os
import tweepy
from typing import Optional

def get_twitter_client() -> Optional[tweepy.Client]:
    """
    Initializes and returns a Tweepy Client using environment variables.
    
    Returns:
        Optional[tweepy.Client]: Configured Twitter client or None if credentials are missing
    """
    consumer_key = os.getenv("TWITTER_API_KEY")
    consumer_secret = os.getenv("TWITTER_API_KEY_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("Error: Twitter API credentials not found in environment variables.")
        print("Please set TWITTER_API_KEY, TWITTER_API_KEY_SECRET, TWITTER_ACCESS_TOKEN, and TWITTER_ACCESS_TOKEN_SECRET.")
        return None

    try:
        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        # Optionally verify credentials to ensure they work
        # This is commented out to avoid making an API call on startup,
        # but can be uncommented for verification
        # client.get_me()
        return client
    except Exception as e:
        print(f"Error initializing Tweepy client: {e}")
        return None