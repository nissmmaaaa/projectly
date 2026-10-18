import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from retrieval.resource_reranker import rerank_resources
from recommendation.resource_recommender import recommend_resources

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def retrieve_resources(project_idea, resources, top_k=5):

    if not resources:
        return []

    resource_texts = []

    for resource in resources:
        text = f"""
        Title: {resource.get('title', '')}
        Description: {resource.get('description', '')}
        Channel: {resource.get('channel', '')}
        """

        resource_texts.append(text)

    resource_embeddings = model.encode(
        resource_texts,
        normalize_embeddings=True
    )

    resource_embeddings = np.asarray(
        resource_embeddings,
        dtype="float32"
    )

    index = faiss.IndexFlatIP(
        resource_embeddings.shape[1]
    )

    index.add(resource_embeddings)

    query_embedding = model.encode(
        [project_idea],
        normalize_embeddings=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    k = min(top_k, len(resources))

    scores, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for score, position in zip(scores[0], indices[0]):
        resource = resources[position].copy()
        resource["similarity_score"] = float(score)
        results.append(resource)

    reranked_resources = rerank_resources(
    project_idea,
    results,
    top_k=len(results)
)

    return recommend_resources(
        reranked_resources,
        top_k=top_k
    )