"""
RSS Feed Configuration

This module defines all RSS feeds to be monitored by the news pulling system.
Using Python with TypedDict for type safety and IDE support.

To add a new feed:
1. Add feed name constant to FeedNames class
2. Add feed configuration to RSS_FEEDS list using the constant
3. Add prompt mapping in llm_prompts.py using the same constant
4. Set enabled=True to activate

Changes take effect on next DAG run.
"""

from typing import TypedDict, List, Dict
from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv("token.env")

class FeedNames:
    """
    RSS Feed name constants

    Use these constants in both RSS_FEEDS and llm_prompts.py
    to prevent typos and maintain consistency.

    When adding a new feed:
    1. Add constant here
    2. Use it in RSS_FEEDS below
    3. Use it in llm_prompts.RSS_FEED_PROMPTS
    """
    REDDIT_ML = "Reddit MachineLearning Feed"
    NEWSLETTER_ELVIS = "AI Newsletter - elvis saravia"


class RSSFeed(TypedDict):
    """
    RSS Feed configuration structure

    Attributes:
        name: Display name for the RSS feed
        url: RSS feed URL
        enabled: Whether to fetch this feed (default: True)
        count: Number of articles to fetch per run (default: 3)
    """
    name: str
    url: str
    enabled: bool
    count: int


# RSS Feed List
# Add new feeds here following the RSSFeed structure
# IMPORTANT: Use FeedNames constants for the "name" field
# RSS_FEEDS: List[RSSFeed] = [
#     {
#         "name": FeedNames.REDDIT_ML,
#         "url": "https://www.reddit.com/r/machinelearningnews/.rss",
#         "enabled": True,
#         "count": 3,
#     },
#     {
#         "name": FeedNames.NEWSLETTER_ELVIS,
#         "url": "https://nlp.elvissaravia.com/feed",
#         "enabled": True,
#         "count": 3,
#     },
#     # Add more feeds here:
#     # {
#     #     "name": FeedNames.YOUR_FEED,  # Add constant to FeedNames first
#     #     "url": "https://example.com/feed.rss",
#     #     "enabled": True,
#     #     "count": 3,
#     # },
# ]

RSSFeed = Dict[str, object]

def fetch_rss_feeds_from_notion(database_id: str, notion_token: str) -> List[RSSFeed]:
    notion = Client(auth=notion_token)

    results = []
    has_more = True
    start_cursor = None

    while has_more:
        params = {
            "filter": {
                "property": "object",
                "value": "page"
            },
            "page_size": 100
        }
        if start_cursor:
            params["start_cursor"] = start_cursor

        response = notion.search(**params)

        for page in response["results"]:
            parent = page.get("parent", {})
            page_db_id = parent.get("database_id", "").replace("-", "")
            target_db_id = database_id.replace("-", "")
            if page_db_id != target_db_id:
                continue

            props = page["properties"]

            # Content Type 필터링
            content_type_prop = props.get("Content Type", {})
            content_type = ""
            if content_type_prop.get("type") == "select":
                select = content_type_prop.get("select")
                if select:
                    content_type = select.get("name", "")
            if content_type != "Substack":
                continue

            # Website Name (title)
            name_prop = props.get("Website Name", {})
            name = ""
            if name_prop.get("type") == "title":
                title_arr = name_prop.get("title", [])
                if title_arr:
                    name = title_arr[0]["plain_text"]

            # URL
            url_prop = props.get("URL", {})
            url = url_prop.get("url", "")

            if not name or not url:
                continue

            results.append({
                "name": name,
                "url": url,
                "enabled": True,
                "count": 3,
            })

        has_more = response.get("has_more", False)
        start_cursor = response.get("next_cursor")

    return results

def get_enabled_feeds() -> List[RSSFeed]:
    """
    Get list of enabled RSS feeds

    Returns:
        List of enabled RSS feeds
    """
    RSS_FEEDS = fetch_rss_feeds_from_notion(
        database_id="1a2f199edf7c8020965ad7d8e22c45cb",
        notion_token= os.environ["NOTION_TOKEN"]
    )

    # return [feed for feed in RSS_FEEDS if feed.get("enabled", True)]
    return RSS_FEEDS

print(get_enabled_feeds())

# def get_all_feeds() -> List[RSSFeed]:
#     """
#     Get all RSS feeds (including disabled ones)

#     Returns:
#         List of all RSS feeds
#     """
#     return RSS_FEEDS
