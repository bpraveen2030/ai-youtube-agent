import re
import feedparser

FEEDS = [
    ("OpenAI", "https://openai.com/news/rss.xml"),
    ("Google AI", "https://blog.google/technology/ai/rss/"),
    ("Microsoft", "https://blogs.microsoft.com/feed/"),
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("MIT Technology Review", "https://www.technologyreview.com/feed/"),
]

KEYWORDS = {
    "ai": 2,
    "artificial intelligence": 2,
    "llm": 2,
    "model": 1,
    "openai": 2,
    "gemini": 2,
    "anthropic": 2,
    "agent": 2,
    "robot": 1,
    "chip": 1,
    "nvidia": 2,
    "research": 1,
}


def _score(title, summary):
    text = f"{title} {summary}".lower()

    score = sum(
        points
        for word, points in KEYWORDS.items()
        if word in text
    )

    if re.search(
        r"\b(releases?|launches?|announces?|acquires?|breakthrough|new)\b",
        text
    ):
        score += 2

    return min(score, 10)


def scout_news():
    results = []
    seen = set()

    for source, url in FEEDS:
        try:
            feed = feedparser.parse(url)

            for item in feed.entries[:20]:
                title = item.get("title", "").strip()
                link = item.get("link", "").strip()

                if not title or not link or link in seen:
                    continue

                seen.add(link)

                summary = re.sub(
                    "<[^>]+>",
                    " ",
                    item.get("summary", "")
                ).strip()

                results.append({
                    "title": title,
                    "url": link,
                    "source": source,
                    "summary": summary[:1500],
                    "published": item.get(
                        "published",
                        item.get("updated", "")
                    ) or "Unknown",
                    "score": _score(title, summary),
                })

        except Exception as exc:
            print(f"Feed error ({source}): {exc}")

    return results
