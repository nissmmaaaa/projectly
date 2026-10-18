
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
from recommendation.dataset_recommender import recommend_datasets
from retrieval.dataset_reranker import rerank_datasets

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def retrieve_datasets(project_idea, datasets, top_k=5):
    if not datasets:
        return []

    dataset_texts = []

    for dataset in datasets:
        text = f"""
        Dataset: {dataset.get('title', '')}
        Description: {dataset.get('description', '')}
        Tags: {', '.join(dataset.get('tags', []))}
        """
        dataset_texts.append(text)

    embeddings = model.encode(
        dataset_texts,
        normalize_embeddings=True
    )
    embeddings = np.asarray(embeddings, dtype="float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    query_embedding = model.encode(
        [project_idea],
        normalize_embeddings=True
    )
    query_embedding = np.asarray(query_embedding, dtype="float32")

    # Retrieve a larger candidate pool before reranking
    k = min(20, len(datasets))
    scores, indices = index.search(query_embedding, k)

    candidates = []

    for score, position in zip(scores[0], indices[0]):
        if position < 0:
            continue

        dataset = datasets[position].copy()
        dataset["similarity_score"] = float(score)
        candidates.append(dataset)

    reranked = rerank_datasets(
    project_idea,
    candidates,
    top_k=len(candidates)
)

    return recommend_datasets(
        reranked,
        top_k=top_k
    )