import argparse
import os

from agents.news_scout import scout_news
from agents.researcher import research_story
from agents.fact_checker import fact_check
from agents.writer import write_script
from agents.metadata import generate_metadata
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

    if args.story:
        index = args.story - 1

        if not 0 <= index < len(stories):
            raise SystemExit("Invalid --story number.")

        story = stories[index]

        print("\nFetching original article...")

        article = fetch_article(story["url"])

        if article.startswith("ARTICLE_BLOCKED"):
            print("\nArticle could not be accessed automatically.")
            print("Using RSS summary instead.")
            article = story["summary"]

        elif article.startswith("ARTICLE_ERROR"):
            print("\nArticle retrieval failed.")
            print("Using RSS summary instead.")
            article = story["summary"]

        elif article.startswith("ARTICLE_EMPTY"):
            print("\nNo article text was extracted.")
            print("Using RSS summary instead.")
            article = story["summary"]

        story_for_research = {
            **story,
            "summary": article,
        }

        print("Researching with local AI...")

        research = research_story(
            story_for_research
        )

        print("Fact-checking...")

        checked = fact_check(research)

        print("Writing script...")

        script = write_script(checked)

        print("Generating metadata...")

        metadata = generate_metadata(
            checked,
            script
        )

        os.makedirs("output", exist_ok=True)

        with open(
            "output/latest.md",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                f"# {story['title']}\n\n"
            )

            f.write(
                "## Source\n"
                f"{story['url']}\n\n"
            )

            f.write(
                "## Research\n"
                f"{research}\n\n"
            )

            f.write(
                "## Fact-check\n"
                f"{checked}\n\n"
            )

            f.write(
                "## Script\n"
                f"{script}\n\n"
            )

            f.write(
                "## Metadata\n"
                f"{metadata}\n"
            )

        print(
            "\nSaved draft: output/latest.md"
        )

        print(
            "Human approval is required "
            "before publishing."
        )


if __name__ == "__main__":
    main()
