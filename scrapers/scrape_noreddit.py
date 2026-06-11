#!/usr/bin/env python3
"""Run scraper sources except Reddit (rate-limited)."""

import json
import sys
sys.path.insert(0, '/Users/m/.openclaw/workspace-tanner/scrapers')

import scrape_all

config = scrape_all.load_config()

all_articles = []

sources = [
    ("HackerNews", scrape_all.scrape_hackernews),
    ("ArXiv", scrape_all.scrape_arxiv),
    ("YouTube", scrape_all.scrape_youtube),
    ("GoogleNews", scrape_all.scrape_google_news),
    ("GitHub", scrape_all.scrape_github_trending),
    ("GitHubReleases", scrape_all.scrape_github_releases),
    ("Mastodon", scrape_all.scrape_mastodon),
    ("RSS", scrape_all.scrape_rss_feeds),
]

for name, fn in sources:
    try:
        arts = fn(config)
        all_articles.extend(arts)
        print(f"[OK] {name}: {len(arts)} articles", file=sys.stderr)
    except Exception as e:
        print(f"[FAIL] {name}: {e}", file=sys.stderr)

print(f"[TOTAL] {len(all_articles)} articles collected", file=sys.stderr)

# Score and save
for article in all_articles:
    article["relevance_score"] = scrape_all.score_article(article, config)
today = scrape_all.date_str()
out_path = scrape_all.RAW_DIR / f"{today}.json"
with open(out_path, "w") as f:
    json.dump({"date": today, "articles": scored}, f)
print(f"[SAVED] {out_path}", file=sys.stderr)
