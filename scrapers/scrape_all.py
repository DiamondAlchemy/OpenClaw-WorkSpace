#!/usr/bin/env python3
"""
Tanner — AI Intelligence Scraper
Scrapes multiple sources for AI news, scores by relevance, outputs unified JSON.

v2 — Fixed: ArXiv retry/backoff, Bluesky disabled (403), GitHub query,
     PapersWithCode→HuggingFace, scoring with diminishing returns.
"""

import json
import os
import sys
import time
import re
import hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote, urlencode
from urllib.error import URLError, HTTPError
from xml.etree import ElementTree
from html import unescape
from email.utils import parsedate_to_datetime

WORKSPACE = Path(__file__).parent.parent
CONFIG_PATH = Path(__file__).parent / "config.json"
RAW_DIR = WORKSPACE / "data" / "raw"
DIGEST_DIR = WORKSPACE / "data" / "digests"

USER_AGENT = "Tanner/1.0 (OpenClaw AI Intelligence Briefer; mailto:alvmedinajr@gmail.com)"
REQUEST_TIMEOUT = 20


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def fetch_url(url, headers=None, retries=2, backoff=3):
    """Fetch URL with error handling, timeout, and retry on 429."""
    hdrs = {"User-Agent": USER_AGENT}
    if headers:
        hdrs.update(headers)
    for attempt in range(retries + 1):
        try:
            req = Request(url, headers=hdrs)
            resp = urlopen(req, timeout=REQUEST_TIMEOUT)
            return resp.read().decode("utf-8", errors="replace")
        except HTTPError as e:
            if e.code == 429 and attempt < retries:
                wait = backoff * (attempt + 1)
                print(f"  [WARN] 429 rate limited, retrying in {wait}s... ({url})", file=sys.stderr)
                time.sleep(wait)
                continue
            print(f"  [WARN] HTTP {e.code} for {url}", file=sys.stderr)
            return None
        except (URLError, Exception) as e:
            print(f"  [WARN] Failed to fetch {url}: {e}", file=sys.stderr)
            return None
    return None


def fetch_json(url, headers=None, retries=2, backoff=3):
    """Fetch URL and parse as JSON."""
    raw = fetch_url(url, headers, retries, backoff)
    if raw:
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"  [WARN] JSON decode error for {url}: {e}", file=sys.stderr)
    return None


def dedup_key(title, url):
    """Generate dedup key from title + url."""
    normalized = re.sub(r'[^a-z0-9]', '', (title or '').lower())
    return hashlib.md5(f"{normalized}:{url}".encode()).hexdigest()


def is_recent(date_str, hours=24):
    """Check if a date string is within the last N hours.

    Handles ISO-8601 (arXiv/HuggingFace) and RFC-822 (RSS/Google News) dates.
    Returns True for empty or unparseable dates (lenient — sources without a
    usable timestamp are kept and gated per-source elsewhere).
    """
    if not date_str:
        return True
    dt = None
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except (ValueError, TypeError):
        try:
            dt = parsedate_to_datetime(date_str)
        except (ValueError, TypeError, IndexError):
            return True
    if dt is None:
        return True
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    return dt > cutoff


# ============================================================
# SOURCE SCRAPERS
# ============================================================

def scrape_reddit(config):
    """Scrape Reddit subreddits for AI posts (hot + rising + new)."""
    articles = []
    cfg = config["sources"]["reddit"]
    if not cfg["enabled"]:
        return articles

    sorts = [cfg["sort"]]
    extra_sorts = cfg.get("extra_sorts", [])
    extra_limit = cfg.get("extra_sort_limit", 25)

    print("[Reddit] Scraping...", file=sys.stderr)
    for sub in cfg["subreddits"]:
        for sort_mode in sorts:
            limit = cfg["limit"]
            url = f"https://www.reddit.com/r/{sub}/{sort_mode}.json?limit={limit}"
            data = fetch_json(url)
            if not data or "data" not in data:
                continue

            for post in data["data"].get("children", []):
                p = post["data"]
                created = datetime.fromtimestamp(p["created_utc"], tz=timezone.utc)
                cutoff = datetime.now(timezone.utc) - timedelta(hours=28)
                if created < cutoff:
                    continue

                articles.append({
                    "title": unescape(p.get("title", "")),
                    "url": f"https://reddit.com{p.get('permalink', '')}",
                    "external_url": p.get("url", ""),
                    "source": f"Reddit r/{sub}",
                    "snippet": (p.get("selftext", "") or "")[:300],
                    "score": p.get("score", 0),
                    "comments": p.get("num_comments", 0),
                    "date": created.isoformat(),
                    "dedup": dedup_key(p.get("title", ""), p.get("permalink", ""))
                })
            time.sleep(1)

        # Extra sorts (rising, new) with lower limit
        for sort_mode in extra_sorts:
            url = f"https://www.reddit.com/r/{sub}/{sort_mode}.json?limit={extra_limit}"
            data = fetch_json(url)
            if not data or "data" not in data:
                continue

            for post in data["data"].get("children", []):
                p = post["data"]
                created = datetime.fromtimestamp(p["created_utc"], tz=timezone.utc)
                cutoff = datetime.now(timezone.utc) - timedelta(hours=28)
                if created < cutoff:
                    continue

                articles.append({
                    "title": unescape(p.get("title", "")),
                    "url": f"https://reddit.com{p.get('permalink', '')}",
                    "external_url": p.get("url", ""),
                    "source": f"Reddit r/{sub} ({sort_mode})",
                    "snippet": (p.get("selftext", "") or "")[:300],
                    "score": p.get("score", 0),
                    "comments": p.get("num_comments", 0),
                    "date": created.isoformat(),
                    "dedup": dedup_key(p.get("title", ""), p.get("permalink", ""))
                })
            time.sleep(1)

    print(f"  [Reddit] Found {len(articles)} recent posts", file=sys.stderr)
    return articles


def scrape_hackernews(config):
    """Scrape Hacker News top and new stories."""
    articles = []
    cfg = config["sources"]["hackernews"]
    if not cfg["enabled"]:
        return articles

    print("[HackerNews] Scraping...", file=sys.stderr)
    for endpoint in cfg["endpoints"]:
        url = f"https://hacker-news.firebaseio.com/v0/{endpoint}.json"
        story_ids = fetch_json(url)
        if not story_ids:
            continue

        for sid in story_ids[:cfg["limit"]]:
            item = fetch_json(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json")
            if not item or item.get("type") != "story":
                continue

            created = datetime.fromtimestamp(item.get("time", 0), tz=timezone.utc)
            cutoff = datetime.now(timezone.utc) - timedelta(hours=28)
            if created < cutoff:
                continue

            articles.append({
                "title": unescape(item.get("title", "")),
                "url": item.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                "external_url": item.get("url", ""),
                "source": "Hacker News",
                "snippet": "",
                "score": item.get("score", 0),
                "comments": item.get("descendants", 0),
                "date": created.isoformat(),
                "dedup": dedup_key(item.get("title", ""), str(sid))
            })
            time.sleep(0.2)

    print(f"  [HackerNews] Found {len(articles)} recent stories", file=sys.stderr)
    return articles


def scrape_arxiv(config):
    """Scrape ArXiv for recent AI papers. Uses HTTPS + retry on 429."""
    articles = []
    cfg = config["sources"]["arxiv"]
    if not cfg["enabled"]:
        return articles

    print("[ArXiv] Scraping...", file=sys.stderr)
    cats = "+OR+".join([f"cat:{c}" for c in cfg["categories"]])
    url = (f"https://export.arxiv.org/api/query?"
           f"search_query={cats}&sortBy=submittedDate"
           f"&sortOrder=descending&max_results={cfg['max_results']}")

    # ArXiv rate limits aggressively — use longer backoff
    raw = fetch_url(url, retries=3, backoff=5)
    if not raw:
        return articles

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    try:
        root = ElementTree.fromstring(raw)
        for entry in root.findall("atom:entry", ns):
            title = entry.findtext("atom:title", "", ns).strip().replace("\n", " ")
            summary = entry.findtext("atom:summary", "", ns).strip().replace("\n", " ")[:300]
            published = entry.findtext("atom:published", "", ns)
            link = ""
            for l in entry.findall("atom:link", ns):
                if l.get("type") == "text/html":
                    link = l.get("href", "")
                    break
            if not link:
                link_el = entry.find("atom:id", ns)
                link = link_el.text if link_el is not None else ""

            articles.append({
                "title": title,
                "url": link,
                "external_url": link,
                "source": "ArXiv",
                "snippet": summary,
                "score": 0,
                "comments": 0,
                "date": published,
                "dedup": dedup_key(title, link)
            })
    except ElementTree.ParseError as e:
        print(f"  [WARN] ArXiv XML parse error: {e}", file=sys.stderr)

    print(f"  [ArXiv] Found {len(articles)} recent papers", file=sys.stderr)
    return articles


def scrape_bluesky(config):
    """Scrape Bluesky for AI posts using public search API."""
    articles = []
    cfg = config["sources"]["bluesky"]
    if not cfg.get("enabled", False):
        return articles

    print("[Bluesky] Scraping...", file=sys.stderr)
    for term in cfg.get("search_terms", []):
        url = (f"https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts"
               f"?q={quote(term)}&limit={cfg.get('limit', 30)}")
        data = fetch_json(url)
        if not data or "posts" not in data:
            print(f"  [Bluesky] No results for '{term}'", file=sys.stderr)
            continue

        for post in data["posts"]:
            record = post.get("record", {})
            author = post.get("author", {})
            handle = author.get("handle", "unknown")
            content = re.sub(r'<[^>]+>', '', record.get("text", ""))
            created = record.get("createdAt", "")
            uri = post.get("uri", "")
            # Convert AT URI to web URL
            if uri:
                parts = uri.split("/")
                if len(parts) >= 3:
                    did = parts[2]
                    rkey = parts[-1] if len(parts) >= 5 else ""
                    post_url = f"https://bsky.app/profile/{did}/post/{rkey}"
                else:
                    post_url = uri
            else:
                post_url = ""

            if not is_recent(created, hours=28):
                continue

            like_count = post.get("likeCount", 0)
            repost_count = post.get("repostCount", 0)

            articles.append({
                "title": content[:120].replace("\n", " "),
                "url": post_url,
                "external_url": post_url,
                "source": f"Bluesky @{handle}",
                "snippet": content[:300],
                "score": like_count + repost_count,
                "comments": post.get("replyCount", 0),
                "date": created,
                "dedup": dedup_key(content[:80], post_url)
            })
        time.sleep(1)

    print(f"  [Bluesky] Found {len(articles)} recent posts", file=sys.stderr)
    return articles


def scrape_youtube(config):
    """Scrape YouTube RSS feeds for AI channels."""
    articles = []
    cfg = config["sources"]["youtube"]
    if not cfg["enabled"]:
        return articles

    print("[YouTube] Scraping...", file=sys.stderr)
    for channel_id, channel_name in cfg["channels"].items():
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        raw = fetch_url(url)
        if not raw:
            continue

        ns = {"atom": "http://www.w3.org/2005/Atom", "media": "http://search.yahoo.com/mrss/"}
        try:
            root = ElementTree.fromstring(raw)
            for entry in root.findall("atom:entry", ns):
                title = entry.findtext("atom:title", "", ns)
                link_el = entry.find("atom:link", ns)
                link = link_el.get("href", "") if link_el is not None else ""
                published = entry.findtext("atom:published", "", ns)

                media_group = entry.find("media:group", ns)
                description = ""
                if media_group is not None:
                    desc_el = media_group.find("media:description", ns)
                    description = (desc_el.text or "")[:300] if desc_el is not None else ""

                if not is_recent(published, hours=48):
                    continue

                articles.append({
                    "title": title,
                    "url": link,
                    "external_url": link,
                    "source": f"YouTube ({channel_name})",
                    "snippet": description,
                    "score": 0,
                    "comments": 0,
                    "date": published,
                    "dedup": dedup_key(title, link)
                })
        except ElementTree.ParseError:
            continue
        time.sleep(0.5)

    print(f"  [YouTube] Found {len(articles)} recent videos", file=sys.stderr)
    return articles


def scrape_google_news(config):
    """Scrape Google News RSS for AI topics."""
    articles = []
    cfg = config["sources"]["google_news"]
    if not cfg["enabled"]:
        return articles

    print("[GoogleNews] Scraping...", file=sys.stderr)
    for query in cfg["queries"]:
        url = f"https://news.google.com/rss/search?q={quote(query)}&hl=en-US&gl=US&ceid=US:en"
        raw = fetch_url(url)
        if not raw:
            continue

        try:
            root = ElementTree.fromstring(raw)
            channel = root.find("channel")
            if channel is None:
                continue
            for item in channel.findall("item"):
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                pub_date = item.findtext("pubDate", "")
                source = item.findtext("source", "Google News")

                articles.append({
                    "title": unescape(title),
                    "url": link,
                    "external_url": link,
                    "source": f"Google News ({source})",
                    "snippet": "",
                    "score": 0,
                    "comments": 0,
                    "date": pub_date,
                    "dedup": dedup_key(title, link)
                })
        except ElementTree.ParseError:
            continue
        time.sleep(0.5)

    print(f"  [GoogleNews] Found {len(articles)} recent articles", file=sys.stderr)
    return articles


def scrape_github_trending(config):
    """Scrape GitHub for trending AI/ML repos created recently."""
    articles = []
    cfg = config["sources"]["github_trending"]
    if not cfg["enabled"]:
        return articles

    print("[GitHub] Scraping...", file=sys.stderr)
    week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")

    # Two queries: recent high-star AI repos + recent LLM repos
    queries = [
        f"created:>{week_ago} stars:>20 (AI OR LLM OR inference)",
        f"created:>{week_ago} stars:>10 (quantization OR MLX OR llama.cpp OR agent)",
    ]

    seen_repos = set()
    for q in queries:
        url = (f"https://api.github.com/search/repositories?"
               f"q={quote(q)}&sort=stars&order=desc&per_page=15")
        data = fetch_json(url, headers={"Accept": "application/vnd.github.v3+json"})
        if not data or "items" not in data:
            continue

        for repo in data["items"]:
            if repo["full_name"] in seen_repos:
                continue
            seen_repos.add(repo["full_name"])

            articles.append({
                "title": f"{repo['full_name']} — {(repo.get('description') or '')[:100]}",
                "url": repo["html_url"],
                "external_url": repo["html_url"],
                "source": "GitHub Trending",
                "snippet": (repo.get("description") or "")[:300],
                "score": repo.get("stargazers_count", 0),
                "comments": repo.get("open_issues_count", 0),
                "date": repo.get("created_at", ""),
                "dedup": dedup_key(repo["full_name"], repo["html_url"])
            })
        time.sleep(2)  # GitHub rate limit

    print(f"  [GitHub] Found {len(articles)} trending repos", file=sys.stderr)
    return articles


def scrape_huggingface_papers(config):
    """Scrape HuggingFace daily papers (replaces PapersWithCode)."""
    articles = []
    cfg = config["sources"].get("huggingface_papers", config["sources"].get("papers_with_code", {}))
    if not cfg.get("enabled", True):
        return articles

    print("[HuggingFace Papers] Scraping...", file=sys.stderr)
    url = "https://huggingface.co/api/daily_papers"
    data = fetch_json(url, headers={"Accept": "application/json"})
    if not data:
        return articles

    limit = cfg.get("limit", 20)
    for paper_entry in data[:limit]:
        paper = paper_entry.get("paper", {})
        title = paper.get("title", "")
        paper_id = paper.get("id", "")
        summary = paper.get("summary", "")[:300]
        published = paper.get("publishedAt", "")
        upvotes = paper_entry.get("numUpvotes", 0)
        link = f"https://huggingface.co/papers/{paper_id}" if paper_id else ""

        articles.append({
            "title": title,
            "url": link,
            "external_url": f"https://arxiv.org/abs/{paper_id}" if paper_id else link,
            "source": "HuggingFace Papers",
            "snippet": summary,
            "score": upvotes,
            "comments": paper_entry.get("numComments", 0),
            "date": published,
            "dedup": dedup_key(title, paper_id)
        })

    print(f"  [HuggingFace Papers] Found {len(articles)} daily papers", file=sys.stderr)
    return articles


def scrape_mastodon(config):
    """Scrape Mastodon (sigmoid.social) for AI posts."""
    articles = []
    cfg = config["sources"]["mastodon"]
    if not cfg["enabled"]:
        return articles

    print("[Mastodon] Scraping...", file=sys.stderr)
    url = f"{cfg['instance']}/api/v1/timelines/public?limit={cfg['limit']}&local=true"
    data = fetch_json(url)
    if not data:
        return articles

    for post in data:
        content = re.sub(r'<[^>]+>', '', post.get("content", ""))
        created = post.get("created_at", "")
        account = post.get("account", {})
        author = account.get("acct", "unknown")
        post_url = post.get("url", "")

        if not is_recent(created, hours=28):
            continue

        articles.append({
            "title": content[:120].replace("\n", " "),
            "url": post_url,
            "external_url": post_url,
            "source": f"Mastodon @{author}",
            "snippet": content[:300],
            "score": post.get("favourites_count", 0) + post.get("reblogs_count", 0),
            "comments": post.get("replies_count", 0),
            "date": created,
            "dedup": dedup_key(content[:80], post_url)
        })

    print(f"  [Mastodon] Found {len(articles)} recent posts", file=sys.stderr)
    return articles


def scrape_github_releases(config):
    """Watch GitHub repos for new releases (version drops, changelogs)."""
    articles = []
    cfg = config["sources"].get("github_releases", {})
    if not cfg.get("enabled", False):
        return articles

    print("[GitHub Releases] Scraping...", file=sys.stderr)
    max_age = cfg.get("max_age_days", 3)
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age)

    for repo in cfg.get("repos", []):
        url = f"https://api.github.com/repos/{repo}/releases?per_page=3"
        data = fetch_json(url, headers={"Accept": "application/vnd.github.v3+json"})
        if not data or not isinstance(data, list):
            continue

        for release in data:
            published = release.get("published_at", "")
            if not published:
                continue
            try:
                pub_dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
            except (ValueError, TypeError):
                continue
            if pub_dt < cutoff:
                continue

            tag = release.get("tag_name", "")
            name = release.get("name", "") or tag
            body = (release.get("body", "") or "")[:400]
            html_url = release.get("html_url", "")
            is_prerelease = release.get("prerelease", False)

            title = f"{repo} {tag}"
            if name and name != tag:
                title = f"{repo} {name} ({tag})"

            articles.append({
                "title": title,
                "url": html_url,
                "external_url": html_url,
                "source": "GitHub Releases",
                "snippet": body,
                "score": release.get("assets", []).__len__() if isinstance(release.get("assets"), list) else 0,
                "comments": 0,
                "date": published,
                "dedup": dedup_key(f"{repo}:{tag}", html_url)
            })
        time.sleep(2)  # GitHub rate limit

    print(f"  [GitHub Releases] Found {len(articles)} recent releases", file=sys.stderr)
    return articles


def scrape_producthunt(config):
    """Scrape ProductHunt for AI/developer tool launches."""
    articles = []
    cfg = config["sources"].get("producthunt", {})
    if not cfg.get("enabled", False):
        return articles

    print("[ProductHunt] Scraping RSS...", file=sys.stderr)
    url = "https://www.producthunt.com/feed"
    raw = fetch_url(url)
    if not raw:
        return articles

    try:
        root = ElementTree.fromstring(raw)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        items = root.findall(".//atom:entry", ns)
        if not items:
            items = root.findall(".//item")

        for item in items[:cfg.get("limit", 30)]:
            title = item.findtext("atom:title", "", ns) or item.findtext("title", "")
            link = ""
            link_el = item.find("atom:link", ns)
            if link_el is not None:
                link = link_el.get("href", "")
            if not link:
                link = item.findtext("link", "")
            summary = item.findtext("atom:summary", "", ns) or item.findtext("atom:content", "", ns) or item.findtext("description", "")
            summary = re.sub(r'<[^>]+>', '', unescape(summary or ""))[:300]
            published = item.findtext("atom:published", "", ns) or item.findtext("pubDate", "")

            # Only include if AI/ML/developer related
            text = f"{title} {summary}".lower()
            ai_keywords = ["ai", "llm", "agent", "ml", "gpt", "claude", "model",
                           "inference", "automation", "copilot", "chatbot", "nlp",
                           "computer vision", "deep learning", "neural", "transformer",
                           "coding", "developer tool", "api", "sdk"]
            if not any(kw in text for kw in ai_keywords):
                continue

            if not is_recent(published, hours=48):
                continue

            articles.append({
                "title": unescape(title),
                "url": link,
                "external_url": link,
                "source": "ProductHunt",
                "snippet": summary,
                "score": 0,
                "comments": 0,
                "date": published,
                "dedup": dedup_key(title, link)
            })
    except ElementTree.ParseError as e:
        print(f"  [WARN] ProductHunt XML parse error: {e}", file=sys.stderr)

    print(f"  [ProductHunt] Found {len(articles)} AI-related launches", file=sys.stderr)
    return articles


def scrape_rss_feeds(config):
    """Scrape generic RSS feeds."""
    articles = []
    cfg = config["sources"]["rss_feeds"]
    if not cfg["enabled"]:
        return articles

    print("[RSS] Scraping...", file=sys.stderr)
    for feed_info in cfg["feeds"]:
        raw = fetch_url(feed_info["url"])
        if not raw:
            continue

        try:
            root = ElementTree.fromstring(raw)
            items = root.findall(".//item")
            if not items:
                ns = {"atom": "http://www.w3.org/2005/Atom"}
                items = root.findall("atom:entry", ns)

            for item in items[:15]:
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                pub_date = item.findtext("pubDate", "")
                description = item.findtext("description", "")

                if not title:
                    ns = {"atom": "http://www.w3.org/2005/Atom"}
                    title = item.findtext("atom:title", "", ns)
                    link_el = item.find("atom:link", ns)
                    link = link_el.get("href", "") if link_el is not None else ""
                    pub_date = item.findtext("atom:published", "", ns) or item.findtext("atom:updated", "", ns)
                    description = item.findtext("atom:summary", "", ns)

                description = re.sub(r'<[^>]+>', '', unescape(description or ""))[:300]

                articles.append({
                    "title": unescape(title),
                    "url": link,
                    "external_url": link,
                    "source": feed_info["name"],
                    "snippet": description,
                    "score": 0,
                    "comments": 0,
                    "date": pub_date,
                    "dedup": dedup_key(title, link)
                })
        except ElementTree.ParseError:
            continue
        time.sleep(0.3)

    print(f"  [RSS] Found {len(articles)} recent articles", file=sys.stderr)
    return articles


# ============================================================
# SCORING ENGINE (v2 — diminishing returns)
# ============================================================

def score_article(article, config):
    """
    Score an article on a ~0-10 scale using diminishing returns.

    First keyword match in a tier = full points.
    Each additional match in the same tier = half the previous bonus.
    This prevents keyword stacking from inflating scores.
    """
    scoring = config["scoring"]
    text = f"{article['title']} {article['snippet']}".lower()
    title_lower = article["title"].lower()

    # Count matches per tier
    t1_matches = sum(1 for kw in scoring["tier1_keywords"] if kw.lower() in text)
    t2_matches = sum(1 for kw in scoring["tier2_keywords"] if kw.lower() in text)
    t3_matches = sum(1 for kw in scoring["tier3_keywords"] if kw.lower() in text)

    # Check for title matches (any tier1 keyword in title = bonus)
    t1_in_title = any(kw.lower() in title_lower for kw in scoring["tier1_keywords"])
    t2_in_title = any(kw.lower() in title_lower for kw in scoring["tier2_keywords"])

    # Diminishing returns: first match = base, each additional = half previous
    # tier1: 3.0, 1.5, 0.75, 0.375... (cap at 6.0)
    # tier2: 1.0, 0.5, 0.25, 0.125... (cap at 2.0)
    # tier3: 0.3, 0.15, 0.075...       (cap at 0.6)
    def diminishing_sum(count, base, cap):
        total = 0
        bonus = base
        for _ in range(count):
            total += bonus
            bonus *= 0.5
            if total >= cap:
                return cap
        return total

    t1_score = diminishing_sum(t1_matches, 3.0, 6.0)
    t2_score = diminishing_sum(t2_matches, 1.0, 2.0)
    t3_score = diminishing_sum(t3_matches, 0.3, 0.6)

    total = t1_score + t2_score + t3_score

    # Title bonus
    if t1_in_title:
        total += 1.5
    elif t2_in_title:
        total += 0.5

    # Upvote bonus (mild — 20% boost if popular)
    if article.get("score", 0) >= 100:
        total *= 1.2
    elif article.get("score", 0) >= 50:
        total *= 1.1

    # Implementation bonus (code/repo mentioned)
    impl_keywords = ["github", "repo", "implementation", "code released", "open source", "pip install"]
    if any(kw in text for kw in impl_keywords):
        total += 1.0

    # Ignore penalty
    for kw in scoring["ignore_keywords"]:
        if kw.lower() in text:
            total -= 2.0

    # De-spam: keyword-stuffed SEO/scam repos that game the keyword scorer
    spam_patterns = [
        "free-desktop-app", "free desktop app", "free-download", "free download",
        "cracked", "nulled", "activation key", "license key free", "mod apk",
        "full version free", "premium free",
    ]
    if any(p in text for p in spam_patterns):
        total -= 5.0

    # Cap on the intended ~0-10 scale (title/impl bonuses could push past 10)
    total = min(total, 10.0)

    return max(0, round(total, 1))


def deduplicate(articles):
    """Remove duplicate articles by dedup key."""
    seen = {}
    unique = []
    for a in articles:
        key = a.get("dedup", "")
        if key and key in seen:
            if a.get("relevance_score", 0) > seen[key].get("relevance_score", 0):
                unique = [x for x in unique if x["dedup"] != key]
                unique.append(a)
                seen[key] = a
        else:
            seen[key] = a
            unique.append(a)
    return unique


SEEN_PATH = WORKSPACE / "data" / "seen_keys.json"


def filter_already_seen(articles, days=14):
    """Drop articles already briefed within the last N days so each brief is
    'new since last time'. Persists a rolling {dedup_key: YYYY-MM-DD} map at
    data/seen_keys.json. Fails open (keeps everything) on any I/O error."""
    today = datetime.now().strftime("%Y-%m-%d")
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    try:
        seen = json.loads(SEEN_PATH.read_text()) if SEEN_PATH.exists() else {}
    except (ValueError, OSError):
        seen = {}
    seen = {k: v for k, v in seen.items() if v >= cutoff}  # prune old
    fresh = []
    for a in articles:
        key = a.get("dedup", "")
        if key and key in seen:
            continue
        fresh.append(a)
        if key:
            seen[key] = today
    try:
        SEEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        SEEN_PATH.write_text(json.dumps(seen))
    except OSError:
        pass
    return fresh


# ============================================================
# MAIN
# ============================================================

def main():
    config = load_config()
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"MONEYPENNY SCRAPER v2 — {today}", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)

    all_articles = []
    scrapers = [
        ("Reddit", scrape_reddit),
        ("HackerNews", scrape_hackernews),
        ("ArXiv", scrape_arxiv),
        ("Bluesky", scrape_bluesky),
        ("YouTube", scrape_youtube),
        ("GoogleNews", scrape_google_news),
        ("GitHub", scrape_github_trending),
        ("GitHubReleases", scrape_github_releases),
        ("HuggingFace", scrape_huggingface_papers),
        ("Mastodon", scrape_mastodon),
        ("ProductHunt", scrape_producthunt),
        ("RSS", scrape_rss_feeds),
    ]

    source_counts = {}
    for name, scraper_fn in scrapers:
        try:
            results = scraper_fn(config)
            source_counts[name] = len(results)
            all_articles.extend(results)
        except Exception as e:
            print(f"  [ERROR] {name} scraper failed: {e}", file=sys.stderr)
            source_counts[name] = -1

    # Score all articles
    for article in all_articles:
        article["relevance_score"] = score_article(article, config)

    # Deduplicate (within this run)
    all_articles = deduplicate(all_articles)

    # Recency filter: drop items whose parseable date is older than the window.
    # Dateless/unparseable items are kept (is_recent is lenient) since several
    # sources are already time-bounded by their API.
    recency_hours = config.get("digest", {}).get("recency_hours", 48)
    before_recency = len(all_articles)
    all_articles = [a for a in all_articles if is_recent(a.get("date"), hours=recency_hours)]
    print(f"[filter] recency<={recency_hours}h dropped {before_recency - len(all_articles)} stale items", file=sys.stderr)

    # Cross-day dedup: drop items already briefed in the last N days so the
    # brief is 'new since last time' (kills day-to-day repetition).
    before_seen = len(all_articles)
    all_articles = filter_already_seen(all_articles, days=config.get("digest", {}).get("seen_window_days", 14))
    print(f"[filter] cross-day dedup dropped {before_seen - len(all_articles)} already-seen items", file=sys.stderr)

    # Sort by relevance score (descending)
    all_articles.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

    # Save raw output
    output = {
        "date": today,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "source_counts": source_counts,
        "total_articles": len(all_articles),
        "articles": all_articles
    }

    raw_path = RAW_DIR / f"{today}.json"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    with open(raw_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    # Print summary
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"SCRAPE COMPLETE", file=sys.stderr)
    print(f"Total articles: {len(all_articles)}", file=sys.stderr)
    print(f"Source breakdown:", file=sys.stderr)
    for src, count in source_counts.items():
        status = f"{count} articles" if count >= 0 else "FAILED"
        print(f"  {src}: {status}", file=sys.stderr)

    above_high = len([a for a in all_articles if a["relevance_score"] >= config["digest"]["high_threshold"]])
    above_med = len([a for a in all_articles if config["digest"]["medium_threshold"] <= a["relevance_score"] < config["digest"]["high_threshold"]])
    print(f"\nHigh relevance (>={config['digest']['high_threshold']}): {above_high}", file=sys.stderr)
    print(f"Medium relevance (>={config['digest']['medium_threshold']}): {above_med}", file=sys.stderr)
    print(f"Output: {raw_path}", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)

    print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
