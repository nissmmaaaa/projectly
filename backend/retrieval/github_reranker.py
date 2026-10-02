from sentence_transformers import CrossEncoder


model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank_github_repositories(project_idea, repositories, top_k=5):

    if not repositories:
        return []

    pairs = []

    for repo in repositories:
        repo_text = f"""
        {repo.get('name', '')}
        {repo.get('description', '')}
        {repo.get('language', '')}
        {', '.join(repo.get('topics', []))}
        """

        pairs.append([project_idea, repo_text])

    scores = model.predict(pairs)

    ranked = []

    for repository, score in zip(repositories, scores):
        repository = repository.copy()
        repository["reranker_score"] = float(score)
        ranked.append(repository)

    ranked.sort(
        key=lambda x: x["reranker_score"],
        reverse=True
    )

    return ranked[:top_k]