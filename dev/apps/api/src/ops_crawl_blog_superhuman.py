import os
import re
import time
import copy
import traceback
from operator import itemgetter
from datetime import datetime

from notion import NotionAgent
from llm_agent import (
    LLMAgentCategoryAndRanking,
    LLMAgentSummary,
)
import utils
from ops_base import OperatorBase
from db_cli import DBClient
from ops_milvus import OperatorMilvus
from ops_notion import OperatorNotion

import requests
from bs4 import BeautifulSoup


class OperatorCrawlBlogSuperhuman(OperatorBase):
    """
    An Operator to crawl Zain Kahn's blog posts.
    - URL: https://www.superhuman.ai/
    - pulling data from source
    - save to local json
    - restore from local json
    - dedup
    - summarization
    - ranking
    - publish
    """

    def _fetch_html(self, url):
        """
        Fetch HTML from URL and parse it with BeautifulSoup

        @param url: URL to fetch
        @return: BeautifulSoup object
        """
        print(f"[fetch_html] Fetching URL: {url}")

        try:
            # Set headers to mimic a browser request
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            print(f"[fetch_html] Successfully fetched and parsed HTML")
            print(
                f"[fetch_html] HTML title: {soup.title.string if soup.title else 'No title'}"
            )
            print(f"[fetch_html] HTML length: {len(response.content)} bytes")

            return soup

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to fetch URL: {url}, error: {e}")
            return None

    def _extract_section_content(self, soup, section_title):
        """
        Extract content from a specific section (like "IN THE KNOW") using DOM structure

        @param soup: BeautifulSoup object
        @param section_title: Section title to find (e.g., "IN THE KNOW")
        @return: Extracted content text or None
        """
        print(f"[extract_section_content] Extracting: {section_title}")

        # Find the section by text
        search_result = soup.find(string=re.compile(section_title, re.IGNORECASE))

        if not search_result:
            print(f"[extract_section_content] Section '{section_title}' not found")
            return None

        # Find the h5 parent tag
        h5_tag = search_result.find_parent("h5")
        if not h5_tag:
            print(f"[extract_section_content] No h5 parent found for '{section_title}'")
            return None

        # Navigate to h5.parent.parent (the container for this section's title)
        level1 = h5_tag.parent  # div wrapping h5
        level2 = level1.parent if level1 else None  # div wrapping that div

        if not level2:
            print(f"[extract_section_content] Cannot reach h5.parent.parent")
            return None

        # Get all next siblings - content is in these siblings
        content_divs = []
        current = level2

        while current:
            current = current.find_next_sibling()
            if not current or not hasattr(current, "name") or not current.name:
                break

            text = current.get_text(strip=True)

            # Check if this sibling contains the next section (h5 tag)
            # If so, we've reached the end of current section
            next_h5 = current.find("h5")
            if next_h5:
                # Reached next section
                break

            # This is content for our section
            content_divs.append(text)

            # Usually 1-2 content divs per section
            if len(content_divs) >= 2:
                break

        if content_divs:
            content = "\n\n".join(content_divs)
            print(
                f"[extract_section_content] Extracted {len(content_divs)} content divs, {len(content)} chars"
            )
            return content

        print(f"[extract_section_content] No content found for '{section_title}'")
        return None

    def _parse_blog_post(self, url, sections_to_extract=None):
        """
        Parse a blog post and extract content from specified sections

        @param url: URL of the blog post
        @param sections_to_extract: List of section titles to extract (default: ["IN THE KNOW", "FROM THE FRONTIER", "TODAY IN AI"])
        @return: Dictionary of {section_title: content}
        """
        if sections_to_extract is None:
            sections_to_extract = ["IN THE KNOW", "FROM THE FRONTIER", "TODAY IN AI"]

        print(f"[parse_blog_post] Parsing: {url}")

        soup = self._fetch_html(url)
        if not soup:
            return {}

        extracted_content = {}

        for section_title in sections_to_extract:
            content = self._extract_section_content(soup, section_title)
            if content:
                extracted_content[section_title] = content

        content = ""
        for key, value in extracted_content.items():
            content += f"##{key}\n{value}\n\n"

        created_at = soup.find(
            "span", string=re.compile(r"([A-Z]?[a-z]+)\s\d{2},\s\d{4}")
        ).get_text(strip=True)
        date_time = datetime.strptime(created_at, "%B %d, %Y")  # e.g. November 22, 2025
        published = date_time.isoformat()
        published_key = date_time.strftime(
            "%Y-%m-%d"
        )  # YYYY-MM-DD (same as ops_rss.py published_key)

        return {
            "title": soup.title.string if soup.title else "No title",
            "content": content,
            "published": published,
            "published_key": published_key,
        }

    def pull(self):
        """
        Pull Superhuman Blog Posts

        @return pages <id, page>
        """
        print("#####################################################")
        print("# Pulling Superhuman Blog Posts")
        print("#####################################################")

        base_url = "https://www.superhuman.ai"

        # 1. Get blog post links from main page
        main_page = self._fetch_html(base_url)

        # 2. Get content from latest blog posts
        post_links = main_page.find_all("a", href=re.compile(r"/p/"))
        valid_links = []
        for link in post_links:
            href = link.get("href", "")
            if href:
                valid_links.append(base_url + href)

        # 3. Get content from latest blog posts
        articles: list[dict] = []
        post_count = min(3, len(valid_links))
        for link in valid_links[:post_count]:
            extracted_content = self._parse_blog_post(link)
            hash_key = f"Superhuman Blog_{extracted_content['title']}_{link}".encode(
                "utf-8"
            )
            article = {
                "id": utils.hashcode_md5(hash_key),
                "source": "Superhuman Blog",
                "list_name": "Superhuman Blog",
                "title": extracted_content["title"],
                "url": link,
                "created_time": datetime.now().isoformat(),
                "summary": extracted_content["content"],  # TODO: currently no summary
                "content": extracted_content["content"],
                "tags": [],  # TODO: currently no tags
                "published": extracted_content["published"],
                "published_key": extracted_content["published_key"],
            }
            articles.append(article)

        pages: dict[str, dict] = {}
        for article in articles:
            page_id = article["id"]
            pages[page_id] = article

        return pages

    def dedup(self, extractedPages, target="inbox"):
        print("#####################################################")
        print("# Dedup RSS")
        print("#####################################################")
        print(f"Number of pages: {len(extractedPages)}")

        client = DBClient()
        deduped_pages = []

        for page_id, page in extractedPages.items():
            title = page["title"]
            list_name = page["list_name"]
            created_time = page["created_time"]

            print(
                f"Dedupping page, title: {title}, list_name: {list_name}, created_time: {created_time}, page_id: {page_id}"
            )

            if not client.get_notion_toread_item_id(
                "superhuman_blog", list_name, page_id
            ):
                deduped_pages.append(page)
                print(
                    f" - No duplicate Superhuman Blog article found, move to next. title: {title}, page_id: {page_id}"
                )

        return deduped_pages

    def filter(self, pages, **kwargs):
        print("#####################################################")
        print("# Filter RSS (After Scoring)")
        print("#####################################################")
        k = kwargs.setdefault("k", 3)
        min_score = kwargs.setdefault("min_score", 4)
        print(f"k: {k}, input size: {len(pages)}, min_score: {min_score}")

        # 1. filter all score >= min_score
        filtered1 = []
        for page in pages:
            relevant_score = page["__relevant_score"]

            if relevant_score < 0 or relevant_score >= min_score:
                filtered1.append(page)

        # 2. get top k
        tops = sorted(
            filtered1, key=lambda page: page["__relevant_score"], reverse=True
        )
        print(f"After sorting: {tops}")

        filtered2 = []
        for i in range(min(k, len(tops))):
            filtered2.append(tops[i])

        print(f"Filter output size: {len(filtered2)}")
        return filtered2

    def score(self, data, **kwargs):
        print("#####################################################")
        print("# Scoring RSS")
        print("#####################################################")
        start_date = kwargs.setdefault("start_date", "")
        max_distance = kwargs.setdefault("max_distance", 0.45)
        print(f"start_date: {start_date}, max_distance: {max_distance}")

        op_milvus = OperatorMilvus()
        client = DBClient()

        scored_list = []

        for page in data:
            try:
                title = page["title"]

                # Get a summary text (at most 1024 chars)
                score_text = (
                    f"{page['title']} - {page['list_name']} - {page['summary']}"
                )
                score_text = score_text[:1024]
                print(f"Scoring page: {title}, score_text: {score_text}")

                relevant_metas = op_milvus.get_relevant(
                    start_date,
                    score_text,
                    topk=2,
                    max_distance=max_distance,
                    db_client=client,
                )

                page_score = op_milvus.score(relevant_metas)

                scored_page = copy.deepcopy(page)
                scored_page["__relevant_score"] = page_score

                scored_list.append(scored_page)
                print(f"RSS article scored {page_score}")

            except Exception as e:
                print(f"[ERROR]: Score page failed, skip: {e}")
                traceback.print_exc()

        print(f"Scored_pages ({len(scored_list)}): {scored_list}")
        return scored_list

    def summarize(self, pages):
        print("#####################################################")
        print("# Summarize RSS Articles")
        print("#####################################################")
        SUMMARY_MAX_LENGTH = int(os.getenv("SUMMARY_MAX_LENGTH", 20000))
        print(f"Number of pages: {len(pages)}")
        print(f"Summary max length: {SUMMARY_MAX_LENGTH}")

        llm_agent = LLMAgentSummary()
        llm_agent.init_prompt()
        llm_agent.init_llm()

        client = DBClient()
        redis_key_expire_time = os.getenv("BOT_REDIS_KEY_EXPIRE_TIME", 604800)

        summarized_pages = []

        for page in pages:
            page_id = page["id"]
            title = page["title"]
            content = page["content"]
            list_name = page["list_name"]
            source_url = page["url"]
            print(f"Summarying page, title: {title}, list_name: {list_name}")
            # print(f"Page content ({len(content)} chars): {content}")

            st = time.time()

            llm_summary_resp = client.get_notion_summary_item_id(
                "rss", list_name, page_id
            )

            if not llm_summary_resp:
                # Double check the content, if empty, load it from
                # the source url. For RSS, we will load content
                # from this entrypoint
                if not content:
                    # First, try to use RSS summary field if available
                    rss_summary = page.get("summary", "")
                    if rss_summary:
                        print("page content is empty, using RSS summary field")
                        content = rss_summary
                    else:
                        print(
                            "page content is empty, fallback to load web page via WebBaseLoader"
                        )

                        try:
                            content = utils.load_web(source_url)
                            print(f"Page content ({len(content)} chars)")

                        except Exception as e:
                            print(
                                f"[ERROR] Exception occurred during utils.load_web(), source_url: {source_url}, {e}"
                            )

                        if not content:
                            print(
                                "[ERROR] Empty Web page loaded via WebBaseLoader, skip it"
                            )
                            continue

                content = content[:SUMMARY_MAX_LENGTH]
                summary = llm_agent.run(content)

                print(
                    f"Cache llm response for {redis_key_expire_time}s, page_id: {page_id}, summary: {summary}"
                )
                client.set_notion_summary_item_id(
                    "rss",
                    list_name,
                    page_id,
                    summary,
                    expired_time=int(redis_key_expire_time),
                )

            else:
                print("Found llm summary from cache, decoding (utf-8) ...")
                summary = utils.bytes2str(llm_summary_resp)

            # assemble summary into page
            summarized_page = copy.deepcopy(page)
            summarized_page["__summary"] = summary

            print(
                f"Used {time.time() - st:.3f}s, Summarized page_id: {page_id}, summary: {summary}"
            )
            summarized_pages.append(summarized_page)

        return summarized_pages

    def rank(self, pages):
        """
        Rank page summary (not the entire content)
        """
        print("#####################################################")
        print("# Rank RSS Articles")
        print("#####################################################")
        ENABLED = utils.str2bool(os.getenv("RSS_ENABLE_CLASSIFICATION", "False"))
        print(f"Number of pages: {len(pages)}, enabled: {ENABLED}")

        llm_agent = LLMAgentCategoryAndRanking()
        llm_agent.init_prompt()
        llm_agent.init_llm()

        client = DBClient()
        redis_key_expire_time = os.getenv("BOT_REDIS_KEY_EXPIRE_TIME", 604800)

        # array of ranged pages
        ranked = []

        for page in pages:
            title = page["title"]
            page_id = page["id"]
            list_name = page["list_name"]
            text = page["__summary"]
            print(f"Ranking page, title: {title}")

            # Let LLM to category and rank
            st = time.time()

            # Parse LLM response and assemble category and rank
            ranked_page = copy.deepcopy(page)

            if not ENABLED:
                ranked_page["__topics"] = []
                ranked_page["__categories"] = []
                ranked_page["__rate"] = -0.02

                ranked.append(ranked_page)
                continue

            llm_ranking_resp = client.get_notion_ranking_item_id(
                "rss", list_name, page_id
            )

            category_and_rank_str = None

            if not llm_ranking_resp:
                print(
                    "Not found category_and_rank_str in cache, fallback to llm_agent to rank"
                )
                category_and_rank_str = llm_agent.run(text)

                print(
                    f"Cache llm response for {redis_key_expire_time}s, page_id: {page_id}"
                )
                client.set_notion_ranking_item_id(
                    "rss",
                    list_name,
                    page_id,
                    category_and_rank_str,
                    expired_time=int(redis_key_expire_time),
                )

            else:
                print("Found category_and_rank_str from cache")
                category_and_rank_str = utils.bytes2str(llm_ranking_resp)

            print(
                f"Used {time.time() - st:.3f}s, Category and Rank: text: {text}, rank_resp: {category_and_rank_str}"
            )

            category_and_rank = utils.fix_and_parse_json(category_and_rank_str)
            print(f"LLM ranked result (json parsed): {category_and_rank}")

            if not category_and_rank:
                print("[ERROR] Cannot parse json string, assign default rating -0.01")
                ranked_page["__topics"] = []
                ranked_page["__categories"] = []
                ranked_page["__rate"] = -0.01
            else:
                ranked_page["__topics"] = [
                    (x["topic"], x.get("score") or 1)
                    for x in category_and_rank["topics"]
                ]
                ranked_page["__categories"] = [
                    (x["category"], x.get("score") or 1)
                    for x in category_and_rank["topics"]
                ]
                ranked_page["__rate"] = category_and_rank["overall_score"]
                ranked_page["__feedback"] = category_and_rank.get("feedback") or ""

            ranked.append(ranked_page)

        print(f"Ranked pages: {ranked}")
        return ranked

    def _get_top_items(self, items: list, k):
        """
        items: [(name, score), ...]
        """
        tops = sorted(items, key=itemgetter(1), reverse=True)
        return tops[:k]

    def push(self, pages, targets, topk=3):
        print("#####################################################")
        print("# Push RSS")
        print("#####################################################")
        print(f"Number of pages: {len(pages)}")
        print(f"Targets: {targets}")
        print(f"Top-K: {topk}")
        print(f"input data: {pages}")
        stat = {
            "total": 0,
            "error": 0,
        }

        for target in targets:
            print(f"Pushing data to target: {target} ...")

            if target == "notion":
                notion_api_key = os.getenv("NOTION_TOKEN")
                notion_agent = NotionAgent(notion_api_key)
                op_notion = OperatorNotion()

                # Get the latest toread database id from index db
                # db_index_id = op_notion.get_index_toread_dbid()

                # database_id = utils.get_notion_database_id_toread(
                #     notion_agent, db_index_id)
                database_id = "2a6f199edf7c809eac47c77106b34c38"

                print(f"Latest ToRead database id: {database_id}")

                if not database_id:
                    print("[ERROR] no index db pages found... skip")
                    break

                for page in pages:
                    stat["total"] += 1

                    try:
                        page_id = page["id"]
                        list_name = page["list_name"]
                        title = page["title"]
                        tags = page["tags"]

                        print(f"Pushing page, title: {title}")

                        topics_topk = [x["term"].replace(",", " ")[:20] for x in tags]
                        topics_topk = topics_topk[:topk]

                        categories_topk = []
                        rating = page.get("__rate") or -1

                        notion_agent.createDatabaseItem_ToRead_RSS(
                            database_id, page, topics_topk, categories_topk, rating
                        )

                        self.markVisited(page_id, source="rss", list_name=list_name)

                    except Exception as e:
                        print(f"[ERROR]: Push to notion failed, skip: {e}")
                        stat["error"] += 1
                        traceback.print_exc()

            else:
                print(f"[ERROR]: Unknown target {target}, skip")

        return stat
