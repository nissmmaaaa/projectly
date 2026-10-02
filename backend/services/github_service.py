import requests


def search_github_repositories(query: str, limit: int = 10):
    url = "https://api.github.com/search/repositories"

    params = {
        "q": query,
        "per_page": limit,
        "sort": "stars",
        "order": "desc"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for repo in data.get("items", []):
        results.append({
            "name": repo.get("full_name"),
            "description": repo.get("description") or "",
            "url": repo.get("html_url"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language"),
            "topics": repo.get("topics", []),
            "source": "GitHub"
        })

    return results