from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import List, Optional
import asyncio
import os

from utils import get_twitter_client

load_dotenv()

# Create a dataclass for our application context
@dataclass
class TwitterContext:
    """Context for the X Twitter Posting MCP server."""
    twitter_client: Optional[object]

@asynccontextmanager
async def twitter_lifespan(server: FastMCP) -> AsyncIterator[TwitterContext]:
    """
    Manages the Twitter client lifecycle.
    
    Args:
        server: The FastMCP server instance
        
    Yields:
        TwitterContext: The context containing the Twitter client
    """
    # Create and return the Twitter client with the helper function in utils.py
    twitter_client = get_twitter_client()
    
    try:
        yield TwitterContext(twitter_client=twitter_client)
    finally:
        # No explicit cleanup needed for the Twitter client
        pass

# Initialize FastMCP server with the Twitter client as context
mcp = FastMCP(
    "x-twitter-posting-mcp",
    description="MCP server for posting tweets and threads to X (Twitter)",
    lifespan=twitter_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),
    port=int(os.getenv("PORT", "8054"))
)        

@mcp.tool()
async def post_tweet(ctx: Context, text: str) -> str:
    """
    Posts a single tweet to X (Twitter).

    Args:
        ctx: The MCP server provided context which includes the Twitter client
        text: The content of the tweet (max 280 characters)
    
    Returns:
        A message indicating success or failure of the tweet posting
    """
    twitter_client = ctx.request_context.lifespan_context.twitter_client
    if not twitter_client:
        return "Error: Twitter client not initialized. Check credentials."

    if len(text) > 280:
        return "Error: Tweet text exceeds 280 characters."
    if not text:
        return "Error: Tweet text cannot be empty."

    try:
        response = twitter_client.create_tweet(text=text)
        tweet_id = response.data.get('id')
        return f"Tweet posted successfully! ID: {tweet_id}"
    except Exception as e:
        return f"Error posting tweet: {str(e)}"

@mcp.tool()
async def post_thread(ctx: Context, tweets: List[str]) -> str:
    """
    Posts a thread of tweets to X (Twitter).
    The first item in the list is the head tweet, subsequent items are replies.

    Args:
        ctx: The MCP server provided context which includes the Twitter client
        tweets: A list of strings, where each string is the content of a tweet in the thread
    
    Returns:
        A message indicating success or failure of the thread posting and the IDs of posted tweets
    """
    if not tweets:
        return "Error: No tweets provided for the thread."

    twitter_client = ctx.request_context.lifespan_context.twitter_client
    if not twitter_client:
        return "Error: Twitter client not initialized. Check credentials."

    last_tweet_id = None
    posted_ids = []

    try:
        # Post the first tweet
        first_tweet_text = tweets[0]
        if len(first_tweet_text) > 280:
             return f"Error: First tweet exceeds 280 characters."
        if not first_tweet_text:
            return f"Error: First tweet cannot be empty."

        response = twitter_client.create_tweet(text=first_tweet_text)
        last_tweet_id = response.data.get('id')
        posted_ids.append(last_tweet_id)

        # Post subsequent tweets as replies
        for i, tweet_text in enumerate(tweets[1:], start=1):
            if len(tweet_text) > 280:
                return f"Error: Tweet {i+1} exceeds 280 characters. Thread partially posted up to tweet ID {last_tweet_id}."
            if not tweet_text:
                 return f"Error: Tweet {i+1} cannot be empty. Thread partially posted up to tweet ID {last_tweet_id}."

            # Add a small delay to avoid rate limiting issues
            await asyncio.sleep(1)

            response = twitter_client.create_tweet(
                text=tweet_text,
                in_reply_to_tweet_id=last_tweet_id
            )
            last_tweet_id = response.data.get('id')
            posted_ids.append(last_tweet_id)

        return f"Thread posted successfully! Tweet IDs: {', '.join(map(str, posted_ids))}"

    except Exception as e:
        if posted_ids:
            return f"Error posting thread (partially posted: {', '.join(map(str, posted_ids))}): {str(e)}"
        else:
            return f"Error posting thread: {str(e)}"

async def main():
    transport = os.getenv("TRANSPORT", "sse")
    if transport == 'sse':
        # Run the MCP server with sse transport
        await mcp.run_sse_async()
    else:
        # Run the MCP server with stdio transport
        await mcp.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())