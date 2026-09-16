import requests
from bs4 import BeautifulSoup


def fetch_article(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        if response.status_code == 403:
            return "ARTICLE_BLOCKED: The website refused automated access."

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside"
        ]):
            tag.decompose()

        paragraphs = []

        for p in soup.find_all("p"):
            text = p.get_text(" ", strip=True)

            if len(text) >= 40:
                paragraphs.append(text)

        article = "\n\n".join(paragraphs)

        if not article:
            return "ARTICLE_EMPTY: No article text could be extracted."

        return article[:12000]

    except requests.RequestException as exc:
        return f"ARTICLE_ERROR: {exc}"
