def recommend_resources(resources, top_k=5):

    if not resources:
        return []

    for resource in resources:

        similarity = resource.get("similarity_score", 0)
        reranker = resource.get("reranker_score", 0)

        resource["recommendation_score"] = (
            0.4 * similarity
            + 0.6 * reranker
        )

    resources.sort(
        key=lambda x: x["recommendation_score"],
        reverse=True
    )

    return resources[:top_k]