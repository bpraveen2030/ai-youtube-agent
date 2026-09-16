import os
from dotenv import load_dotenv

load_dotenv()

CHANNEL_NAME = os.getenv("CHANNEL_NAME", "MathsXMatter")
MIN_STORY_SCORE = int(os.getenv("MIN_STORY_SCORE", "5"))
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "").rstrip("/")
LLM_MODEL = os.getenv("LLM_MODEL", "")
