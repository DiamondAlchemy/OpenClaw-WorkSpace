#!/usr/bin/env python3
"""
Tanner — Digest Generator
Reads raw scrape data and generates a formatted daily digest.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
RAW_DIR = WORKSPACE / "data" / "raw"
DIGEST_DIR = WORKSPACE / "data" / "digests"
CONFIG_PATH = Path(__file__).parent / "config.json"


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def generate_digest(date_str=None):
    config = load_config()
    today = date_str or datetime.now().strftime("%Y-%m-%d")
    raw_path = RAW_DIR / f"{today}.json"

    if not raw_path.exists():
        print(f"No raw data found for {today}. Run scrape_all.py first.", file=sys.stderr)
        sys.exit(1)

    with open(raw_path) as f:
        data = json.load(f)

    articles = data["articles"]
    source_counts = data["source_counts"]
    total = data["total_articles"]

    high_threshold = config["digest"]["high_threshold"]
    med_threshold = config["digest"]["medium_threshold"]
    max_high = config["digest"]["max_high_items"]
    max_med = config["digest"]["max_medium_items"]
    max_watch = config["digest"]["max_watch_items"]

    high_items = [a for a in articles if a["relevance_score"] >= high_threshold][:max_high]
    med_items = [a for a in articles if med_threshold <= a["relevance_score"] < high_threshold][:max_med]
    watch_items = [a for a in articles if 1 <= a["relevance_score"] < med_threshold][:max_watch]

    # Build digest
    lines = []
    lines.append(f"MONEYPENNY DAILY BRIEF -- {today}")
    lines.append("")

    if high_items:
        lines.append("HIGH RELEVANCE")
        for i, a in enumerate(high_items, 1):
            lines.append(f"{i}. {a['title'][:100]} -- {a['source']}")
            if a.get("snippet"):
                lines.append(f"   {a['snippet'][:150]}")
            lines.append(f"   Score: {a['relevance_score']} | {a['url']}")
            lines.append("")
    else:
        lines.append("HIGH RELEVANCE")
        lines.append("No high-signal items today.")
        lines.append("")

    if med_items:
        lines.append("MEDIUM RELEVANCE")
        for i, a in enumerate(med_items, len(high_items) + 1):
            lines.append(f"{i}. {a['title'][:100]} -- {a['source']}")
            if a.get("snippet"):
                lines.append(f"   {a['snippet'][:150]}")
            lines.append(f"   Score: {a['relevance_score']} | {a['url']}")
            lines.append("")

    if watch_items:
        lines.append("WORTH WATCHING")
        for a in watch_items:
            lines.append(f"- {a['title'][:80]} -- {a['source']} -- {a['url']}")
        lines.append("")

    # Footer
    sources_active = [k for k, v in source_counts.items() if v >= 0]
    sources_failed = [k for k, v in source_counts.items() if v < 0]
    lines.append("---")
    lines.append(f"{total} articles scanned | {len(high_items)} high | {len(med_items)} medium | Sources: {', '.join(sources_active)}")
    if sources_failed:
        lines.append(f"Failed sources: {', '.join(sources_failed)}")

    digest_text = "\n".join(lines)

    # Save digest
    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    digest_path = DIGEST_DIR / f"{today}.md"
    with open(digest_path, "w") as f:
        f.write(digest_text)

    print(f"Digest saved to: {digest_path}", file=sys.stderr)
    print(digest_text)


if __name__ == "__main__":
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    generate_digest(date_arg)
