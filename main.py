import argparse
from agents.news_scout import scout_news
from agents.researcher import research_story
from agents.fact_checker import fact_check
from agents.writer import write_script
from agents.metadata import generate_metadata
from tools.database import init_db, save_stories
from config import MIN_STORY_SCORE

def main():
    parser = argparse.ArgumentParser(description="AI YouTube News Agent V1")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--story", type=int, help="Process a shortlist item by number")
    args = parser.parse_args()

    init_db()
    stories = [s for s in scout_news() if s["score"] >= MIN_STORY_SCORE]
    stories.sort(key=lambda x: x["score"], reverse=True)
    stories = stories[:args.limit]
    save_stories(stories)

    if not stories:
        print("No qualifying stories found.")
        return

    print("\nNEWS SHORTLIST")
    print("=" * 70)
    for i, story in enumerate(stories, 1):
        print(f"{i}. [{story['score']}/10] {story['title']}")
        print(f"   {story['source']} | {story['published']}")
        print(f"   {story['url']}")

    if args.story:
        index = args.story - 1
        if not 0 <= index < len(stories):
            raise SystemExit("Invalid --story number.")
        story = stories[index]
        research = research_story(story)
        checked = fact_check(research)
        script = write_script(checked)
        metadata = generate_metadata(checked, script)

        os.makedirs("output", exist_ok=True)
        with open("output/latest.md", "w", encoding="utf-8") as f:
            f.write(f"# {story['title']}\n\n")
            f.write("## Research\n" + research + "\n\n")
            f.write("## Fact-check\n" + checked + "\n\n")
            f.write("## Script\n" + script + "\n\n")
            f.write("## Metadata\n" + metadata + "\n")
        print("\nSaved draft: output/latest.md")
        print("Human approval is required before publishing.")

if __name__ == "__main__":
    import os
    main()
