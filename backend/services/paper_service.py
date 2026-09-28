import requests

from services.arxiv_service import search_arxiv
from services.openalex_service import search_openalex


def search_semantic_scholar(query: str, limit: int = 10):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": query,
        "limit": limit,
        "fields": "title,abstract,authors,year,url,citationCount"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for paper in data.get("data", []):
        results.append({
            "title": paper.get("title"),
            "abstract": paper.get("abstract") or "",
            "authors": [
                author.get("name")
                for author in paper.get("authors", [])
            ],
            "year": paper.get("year"),
            "url": paper.get("url"),
            "citation_count": paper.get("citationCount", 0),
            "source": "Semantic Scholar"
        })

    return results


def search_all_papers(query: str, limit: int = 10):
    semantic_scholar_results = search_semantic_scholar(query, limit)
    arxiv_results = search_arxiv(query, limit)
    openalex_results = search_openalex(query, limit)

    return (
        semantic_scholar_results
        + arxiv_results
        + openalex_results
    )