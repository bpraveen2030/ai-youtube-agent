from agents.news_scout import scout_news


if __name__ == "__main__":
    stories = scout_news()

    for story in stories:
        print(story)
