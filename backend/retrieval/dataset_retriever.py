import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def retrieve_datasets(project_idea, datasets, top_k=5):

    if not datasets:
        return []

    # Build searchable text directly from dataset information
    dataset_texts = []

    for dataset in datasets:
        text = f"""
        Dataset: {dataset.get('id', '')}
        Description: {dataset.get('description', '')}
        Tags: {', '.join(dataset.get('tags', []))}
        """
        dataset_texts.append(text)

    # Create embeddings
    dataset_embeddings = model.encode(
        dataset_texts,
        normalize_embeddings=True
    )

    dataset_embeddings = np.asarray(
        dataset_embeddings,
        dtype="float32"
    )

    # FAISS index
    index = faiss.IndexFlatIP(dataset_embeddings.shape[1])
    index.add(dataset_embeddings)

    # Embed user query
    query_embedding = model.encode(
        [project_idea],
        normalize_embeddings=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    # Search
    k = min(top_k, len(datasets))

    scores, indices = index.search(
        query_embedding,
        k
    )

    # Return ranked datasets
    results = []

    for score, position in zip(scores[0], indices[0]):
        dataset = datasets[position].copy()
        dataset["similarity_score"] = float(score)
        results.append(dataset)

    return results