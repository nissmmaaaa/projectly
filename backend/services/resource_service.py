from services.youtube_service import search_youtube


def search_all_resources(query: str, limit: int = 10):
    youtube_results = search_youtube(query, limit)

    return youtube_results
from services.youtube_service import search_youtube


OFFICIAL_DOCS = [
    {
        "title": "PyTorch Tutorials",
        "description": "Official tutorials for deep learning, neural networks, and model training.",
        "url": "https://docs.pytorch.org/tutorials/",
        "source": "PyTorch Documentation",
    },
    {
        "title": "Hugging Face Transformers Documentation",
        "description": "Documentation for pretrained transformer models, OCR, and NLP.",
        "url": "https://huggingface.co/docs/transformers/",
        "source": "Hugging Face Documentation",
    },
    {
        "title": "OpenCV Documentation",
        "description": "Official computer vision documentation for image processing and document preprocessing.",
        "url": "https://docs.opencv.org/",
        "source": "OpenCV Documentation",
    },
]


def search_all_resources(query: str, limit: int = 10):
    results = []

    try:
        results.extend(search_youtube(query, limit))
    except Exception as e:
        print(f"YouTube search failed: {e}")

    query_words = set(query.lower().split())

    for doc in OFFICIAL_DOCS:
        text = f"{doc['title']} {doc['description']}".lower()

        if any(word in text for word in query_words):
            results.append(doc)

    return results
