import requests
from bs4 import BeautifulSoup


def fetch_article(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

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

    return article[:12000]
