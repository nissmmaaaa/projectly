import requests
import xml.etree.ElementTree as ET


def search_arxiv(query: str, limit: int = 10):
    url = "https://export.arxiv.org/api/query"

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": limit,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    root = ET.fromstring(response.text)

    namespace = {
        "atom": "http://www.w3.org/2005/Atom"
    }

    results = []

    for entry in root.findall("atom:entry", namespace):
        results.append({
            "title": entry.findtext("atom:title", default="", namespaces=namespace).strip(),
            "abstract": entry.findtext("atom:summary", default="", namespaces=namespace).strip(),
            "authors": [
                author.findtext("atom:name", default="", namespaces=namespace)
                for author in entry.findall("atom:author", namespace)
            ],
            "year": (
                entry.findtext("atom:published", default="", namespaces=namespace)[:4]
                or None
            ),
            "url": entry.findtext("atom:id", default="", namespaces=namespace),
            "citation_count": 0,
            "source": "arXiv"
        })

    return results