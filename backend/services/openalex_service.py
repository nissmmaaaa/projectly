import requests


def search_openalex(query: str, limit: int = 10):
    url = "https://api.openalex.org/works"

    params = {
        "search": query,
        "per-page": limit
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for work in data.get("results", []):
        results.append({
            "title": work.get("title") or "",
            "abstract": "",
            "authors": [
                author.get("author", {}).get("display_name")
                for author in work.get("authorships", [])
                if author.get("author")
            ],
            "year": work.get("publication_year"),
            "url": work.get("doi") or work.get("id"),
            "citation_count": work.get("cited_by_count", 0),
            "source": "OpenAlex"
        })

    return results