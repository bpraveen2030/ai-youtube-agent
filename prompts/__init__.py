from pathlib import Path

ROOT = Path(__file__).parent

def load_prompt(name):
    return (ROOT / name).read_text(encoding="utf-8")
