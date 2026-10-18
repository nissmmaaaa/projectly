
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank_datasets(project_idea, datasets, top_k=5):
    if not datasets:
        return []

    pairs = []

    for dataset in datasets:
        dataset_text = f"""
        Title: {dataset.get('title', '')}
        Description: {dataset.get('description', '')}
        Tags: {', '.join(dataset.get('tags', []))}
        """

        pairs.append([project_idea, dataset_text])

    scores = model.predict(pairs)

    ranked = []

    for dataset, score in zip(datasets, scores):
        dataset = dataset.copy()
        dataset["reranker_score"] = float(score)
        ranked.append(dataset)

    ranked.sort(
        key=lambda dataset: dataset["reranker_score"],
        reverse=True
    )

    return ranked[:top_k]
