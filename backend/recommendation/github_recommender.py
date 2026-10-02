def recommend_github_repositories(repositories, top_k=5):

    if not repositories:
        return []

    for repo in repositories:

        similarity = repo.get("similarity_score", 0)
        reranker = repo.get("reranker_score", 0)
        stars = repo.get("stars", 0)

        star_score = min(stars / 1000, 1)

        repo["recommendation_score"] = (
            0.4 * similarity
            + 0.5 * reranker
            + 0.1 * star_score
        )

    repositories.sort(
        key=lambda x: x["recommendation_score"],
        reverse=True
    )

    return repositories[:top_k]