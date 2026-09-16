from agents.researcher import _llm
from prompts import load_prompt


def write_script(fact_checked_research):
    prompt = load_prompt("script.txt").format(
        research=fact_checked_research
    )

    return _llm(prompt)
