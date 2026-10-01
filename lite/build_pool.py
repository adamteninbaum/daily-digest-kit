"""Build the shared headline pool for the Daily Digest Lite page.

Usage: python3 lite/build_pool.py OUT.json [--hours 24]
Runs free discovery for every intake topic (Google News per topic, plus Hacker News,
Techmeme and Hugging Face papers) and writes one deduped pool:
  {"generated_at": ISO, "hours": N, "topics": [...], "items": [
     {"id", "topic", "title", "url", "source", "publisher", "summary", "points"}]}
Each viewer's own Claude picks from this pool on the Lite page, by id, so links are never invented.
Google News links stay as Google wrappers (they open the article in a browser).
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import quote

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from discover import get, hacker_news, hf_papers, rss_items  # noqa: E402

# Topic name on the page -> Google News search query
TOPICS = {
    "AI": "artificial intelligence", "Tech & gadgets": "technology gadgets",
    "Business & markets": "stock market business", "Startups": "startup funding",
    "Personal finance": "personal finance", "US politics": "US politics",
    "World news": "world news", "Law": "law court ruling", "Science": "science discovery",
    "Space": "space NASA", "Health & fitness": "health fitness", "Climate": "climate",
    "Sports": "sports", "Film & TV": "movies TV", "Music": "music", "Gaming": "video games",
    "Design & creative": "design creative", "Food & cooking": "food cooking",
    "Travel": "travel", "Books": "books authors",
}
PER_TOPIC = 10


def google_news(topic, query):
    url = ("https://news.google.com/rss/search?q=" + quote(f"{query} when:1d")
           + "&hl=en-US&gl=US&ceid=US:en")
    root = ET.fromstring(get(url).content)
    out = []
    for item in root.iter("item"):
        src = item.find("source")
        publisher = (src.text or "").strip() if src is not None else ""
        title = (item.findtext("title") or "").strip()
        if publisher and title.endswith(" - " + publisher):
            title = title[: -len(publisher) - 3]
        out.append({"topic": topic, "title": title, "url": (item.findtext("link") or "").strip(),
                    "source": "Google News", "publisher": publisher, "summary": "", "points": 0})
        if len(out) >= PER_TOPIC:
            break
    return out


def norm(t):
    return re.sub(r"[^a-z0-9 ]", "", t.lower())[:70]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--hours", type=int, default=24)
    args = ap.parse_args()
    items, errors = [], {}
    for topic, query in TOPICS.items():
        try:
            items += google_news(topic, query)
        except Exception as e:
            errors[topic] = f"{type(e).__name__}: {e}"[:200]
    try:
        for h in hacker_news(args.hours):
            items.append({"topic": "Tech & gadgets", "title": h["title"], "url": h["url"],
                          "discussion": h["discussion"], "source": "Hacker News",
                          "publisher": "Hacker News", "summary": "", "points": h["points"]})
    except Exception as e:
        errors["hacker_news"] = f"{type(e).__name__}: {e}"[:200]
    try:
        for t in rss_items("https://www.techmeme.com/feed.xml", "Techmeme", 15):
            items.append({"topic": "Tech & gadgets", "title": t["title"], "url": t["url"],
                          "source": "Techmeme", "publisher": "Techmeme",
                          "summary": t.get("summary", "")[:200], "points": 0})
    except Exception as e:
        errors["techmeme"] = f"{type(e).__name__}: {e}"[:200]
    try:
        for p in hf_papers():
            items.append({"topic": "AI", "title": p["title"], "url": p["url"],
                          "source": "Hugging Face papers", "publisher": "Hugging Face",
                          "summary": "", "points": p.get("upvotes", 0)})
    except Exception as e:
        errors["hf_papers"] = f"{type(e).__name__}: {e}"[:200]

    seen, pool = set(), []
    for i in items:
        key = norm(i["title"])
        if not i["title"] or not i["url"] or key in seen:
            continue
        seen.add(key)
        i["id"] = hashlib.sha1(i["url"].encode()).hexdigest()[:8]
        pool.append(i)
    data = {"generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "hours": args.hours, "topics": list(TOPICS), "items": pool, "errors": errors}
    with open(args.out, "w") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(pool)} items, {len(errors)} errors -> {args.out}")
    if errors:
        print(json.dumps(errors, indent=1))


if __name__ == "__main__":
    main()
