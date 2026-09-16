# AI YouTube News Agent

Python-first V1 for a faceless Tech & AI News YouTube channel.

## V1 pipeline
1. Discover AI/tech news from RSS feeds
2. Remove duplicates and score stories
3. Save stories to SQLite
4. Optionally generate research, fact-checking, a script and metadata with an LLM
5. Stop for human approval before publishing

Video rendering, thumbnails, YouTube upload and analytics are intentionally left for later versions.

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py --limit 10
```

For LLM generation, configure `LLM_API_KEY`, `LLM_BASE_URL`, and `LLM_MODEL` in `.env`.

Never commit `.env` or API keys.
