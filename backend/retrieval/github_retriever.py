import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from retrieval.github_reranker import rerank_github_repositories
from recommendation.github_recommender import recommend_github_repositories

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def retrieve_github_repositories(project_idea, repositories, top_k=5):

    if not repositories:
        return []

    repo_texts = []

    for repo in repositories:
        text = f"""
        Repository: {repo.get('name', '')}
        Description: {repo.get('description', '')}
        Language: {repo.get('language', '')}
        Topics: {', '.join(repo.get('topics', []))}
        """

        repo_texts.append(text)

    repo_embeddings = model.encode(
        repo_texts,
        normalize_embeddings=True
    )

    repo_embeddings = np.asarray(
        repo_embeddings,
        dtype="float32"
    )

    index = faiss.IndexFlatIP(
        repo_embeddings.shape[1]
    )

    index.add(repo_embeddings)

    query_embedding = model.encode(
        [project_idea],
        normalize_embeddings=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    k = min(top_k, len(repositories))

    scores, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for score, position in zip(scores[0], indices[0]):
        repository = repositories[position].copy()
        repository["similarity_score"] = float(score)
        results.append(repository)

    reranked_repositories = rerank_github_repositories(
    project_idea,
    results,
    top_k=len(results)
)

    return recommend_github_repositories(
        reranked_repositories,
        top_k=top_k
    )