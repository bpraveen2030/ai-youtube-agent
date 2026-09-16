from agents.researcher import _llm
from prompts import load_prompt


def fact_check(research):
    prompt = load_prompt("fact_check.txt").format(
        research=research
    )

    return _llm(prompt)
