from agents.researcher import _llm
from prompts import load_prompt


def generate_metadata(research, script):
    prompt = load_prompt("metadata.txt").format(
        research=research,
        script=script
    )

    return _llm(prompt)
