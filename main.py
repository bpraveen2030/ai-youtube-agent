import argparse
import os

from agents.news_scout import scout_news
from agents.researcher import research_story
from tools.article_reader import fetch_article
from tools.database import init_db, save_stories
from config import MIN_STORY_SCORE


def main():
    parser = argparse.ArgumentParser(
        description="AI YouTube News Agent V1"
    )

    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument(
        "--story",
        type=int,
        help="Process a shortlist item by number"
    )

    args = parser.parse_args()

    init_db()

    stories = [
        s for s in scout_news()
        if s["score"] >= MIN_STORY_SCORE
    ]

    stories.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    stories = stories[:args.limit]

    save_stories(stories)

    if not stories:
        print("No qualifying stories found.")
        return

    print("\nNEWS SHORTLIST")
    print("=" * 70)

    for i, story in enumerate(stories, 1):
        print(
            f"{i}. [{story['score']}/10] "
            f"{story['title']}"
        )
        print(
            f"   {story['source']} | "
            f"{story['published']}"
        )
        print(f"   {story['url']}")

    if not args.story:
        return

    index = args.story - 1

    if not 0 <= index < len(stories):
        raise SystemExit("Invalid --story number.")

    story = stories[index]

    print("\nFetching original article...")

    article = fetch_article(story["url"])

    if article.startswith("ARTICLE_"):
        print("Using RSS summary.")
        article = story["summary"]
    else:
        print("Article text retrieved.")

    story_for_research = {
        **story,
        "summary": article,
    }

    print("Generating research with local AI...")

    research = research_story(story_for_research)

    os.makedirs("output", exist_ok=True)

    with open(
        "output/latest.md",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(f"# {story['title']}\n\n")
        f.write(f"## Source\n{story['url']}\n\n")
        f.write(f"## Research\n{research}\n")

    print("\nSaved: output/latest.md")
    print("Human approval is required before publishing.")


if __name__ == "__main__":
    main()
