from sentence_transformers import CrossEncoder


model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank_papers(project_idea, papers, top_k=5):

    if not papers:
        return []

    pairs = []

    for paper in papers:
        paper_text = f"""
        {paper.get('title', '')}
        {paper.get('abstract', '')}
        """

        pairs.append([project_idea, paper_text])

    scores = model.predict(pairs)

    ranked = []

    for paper, score in zip(papers, scores):
        paper = paper.copy()
        paper["reranker_score"] = float(score)
        ranked.append(paper)

    ranked.sort(
        key=lambda x: x["reranker_score"],
        reverse=True
    )

    return ranked[:top_k]