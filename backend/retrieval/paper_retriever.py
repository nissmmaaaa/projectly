import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from retrieval.paper_reranker import rerank_papers
from recommendation.paper_recommender import recommend_papers


model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def retrieve_papers(project_idea, papers, top_k=5):

    if not papers:
        return []

    paper_texts = []

    for paper in papers:
        text = f"""
        Title: {paper.get('title', '')}
        Abstract: {paper.get('abstract', '')}
        Authors: {', '.join(paper.get('authors', []))}
        """

        paper_texts.append(text)

    paper_embeddings = model.encode(
        paper_texts,
        normalize_embeddings=True
    )

    paper_embeddings = np.asarray(
        paper_embeddings,
        dtype="float32"
    )

    index = faiss.IndexFlatIP(
        paper_embeddings.shape[1]
    )

    index.add(paper_embeddings)

    query_embedding = model.encode(
        [project_idea],
        normalize_embeddings=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    k = min(top_k, len(papers))

    scores, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for score, position in zip(
        scores[0],
        indices[0]
    ):
        paper = papers[position].copy()

        paper["similarity_score"] = float(score)

        results.append(paper)

    reranked_papers = rerank_papers(
    project_idea,
    results,
    top_k=len(results)
)

    return recommend_papers(
    reranked_papers,
    top_k=top_k
)