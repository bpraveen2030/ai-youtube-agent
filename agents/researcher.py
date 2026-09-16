import requests

from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
from prompts import load_prompt


def _llm(prompt):
    if not (LLM_API_KEY and LLM_BASE_URL and LLM_MODEL):
        return (
            "LLM is not configured yet. "
            "Use the source URL and summary for manual research."
        )

    response = requests.post(
        f"{LLM_BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": LLM_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a careful technology news researcher. "
                        "Never invent facts, quotes, numbers or sources."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.2,
        },
        timeout=90,
    )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


def research_story(story):
    prompt = load_prompt("research.txt").format(
        title=story["title"],
        source=story["source"],
        url=story["url"],
        summary=story["summary"],
    )

    return _llm(prompt)
