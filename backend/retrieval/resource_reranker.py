from sentence_transformers import CrossEncoder


model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank_resources(project_idea, resources, top_k=5):

    if not resources:
        return []

    pairs = []

    for resource in resources:
        resource_text = f"""
        {resource.get('title', '')}
        {resource.get('description', '')}
        {resource.get('channel', '')}
        """

        pairs.append([project_idea, resource_text])

    scores = model.predict(pairs)

    ranked = []

    for resource, score in zip(resources, scores):
        resource = resource.copy()
        resource["reranker_score"] = float(score)
        ranked.append(resource)

    ranked.sort(
        key=lambda x: x["reranker_score"],
        reverse=True
    )

    return ranked[:top_k]