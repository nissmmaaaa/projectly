
def recommend_datasets(datasets, top_k=5):
    if not datasets:
        return []

    for dataset in datasets:
        similarity = dataset.get("similarity_score", 0)
        reranker = dataset.get("reranker_score", 0)

        # Normalize semantic similarity from [-1, 1] to [0, 1]
        similarity_score = (similarity + 1) / 2
        similarity_score = max(0, min(similarity_score, 1))

        # Cross-Encoder scores are not probabilities.
        # Convert them to a bounded score for combining signals.
        reranker_score = 1 / (1 + __import__("math").exp(
            -max(-20, min(reranker, 20))
        ))

        # Quality signals vary by source
        downloads = dataset.get("downloads", 0) or 0
        likes = dataset.get("likes", dataset.get("votes", 0)) or 0
        votes = dataset.get("votes", 0) or 0

        import math
        popularity_score = (
            math.log1p(max(0, downloads))
            + math.log1p(max(0, likes))
            + math.log1p(max(0, votes))
        ) / 30

        popularity_score = min(popularity_score, 1)

        dataset["recommendation_score"] = (
            0.35 * similarity_score
            + 0.50 * reranker_score
            + 0.15 * popularity_score
        )

    return sorted(
        datasets,
        key=lambda dataset: dataset["recommendation_score"],
        reverse=True
    )[:top_k]
