"""
RSS Feed Configuration

This module defines all RSS feeds to be monitored by the news pulling system.
Using Python with TypedDict for type safety and IDE support.

To add a new feed:
1. Add a new dictionary to RSS_FEEDS list
2. Follow the RSSFeed type structure
3. Set enabled=True to activate

Changes take effect on next DAG run.
"""

from typing import TypedDict, List


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
RSS_FEEDS: List[RSSFeed] = [
    {
        "name": "Reddit MachineLearning Feed",
        "url": "https://www.reddit.com/r/machinelearningnews/.rss",
        "enabled": True,
        "count": 3,
    },
    {
        "name": "AI Newsletter - elvis saravia",
        "url": "https://nlp.elvissaravia.com/feed",
        "enabled": True,
        "count": 3,
    },
    # Add more feeds here:
    # {
    #     "name": "Your Feed Name",
    #     "url": "https://example.com/feed.rss",
    #     "enabled": True,
    #     "count": 3,
    # },
]


def get_enabled_feeds() -> List[RSSFeed]:
    """
    Get list of enabled RSS feeds

    Returns:
        List of enabled RSS feeds
    """
    return [feed for feed in RSS_FEEDS if feed.get("enabled", True)]


def get_all_feeds() -> List[RSSFeed]:
    """
    Get all RSS feeds (including disabled ones)

    Returns:
        List of all RSS feeds
    """
    return RSS_FEEDS
