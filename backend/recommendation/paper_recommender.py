def recommend_papers(papers, top_k=5):

    if not papers:
        return []

    for paper in papers:

        similarity = paper.get("similarity_score", 0)
        reranker = paper.get("reranker_score", 0)
        citations = paper.get("citation_count", 0)

        citation_score = min(citations / 100, 1)

        paper["recommendation_score"] = (
            0.4 * similarity
            + 0.5 * reranker
            + 0.1 * citation_score
        )

    papers.sort(
        key=lambda x: x["recommendation_score"],
        reverse=True
    )

    return papers[:top_k]