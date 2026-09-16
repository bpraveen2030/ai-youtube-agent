 from llama_cpp import Llama

from prompts import load_prompt


MODEL_PATH = "models/model.gguf"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    verbose=False
)


def _llm(prompt):
    response = llm(
        prompt,
        max_tokens=700,
        temperature=0.2
    )

    return response["choices"][0]["text"].strip()


def research_story(story):
    prompt = load_prompt("research.txt").format(
        title=story["title"],
        source=story["source"],
        url=story["url"],
        summary=story["summary"],
    )

    return _llm(prompt)
