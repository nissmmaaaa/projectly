
import requests

from services.kaggle_service import search_kaggle_datasets


def search_huggingface_datasets(query: str, limit: int = 10):
    url = "https://huggingface.co/api/datasets"

    params = {
        "search": query,
        "limit": limit,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=20
        )
        response.raise_for_status()
        datasets = response.json()

    except requests.RequestException as e:
        print(f"Hugging Face search failed: {e}")
        return []

    results = []

    for dataset in datasets:
        dataset_id = dataset.get("id")

        results.append({
            "id": dataset_id,
            "title": dataset_id or "",
            "author": dataset.get("author"),
            "description": dataset.get("description") or "",
            "downloads": dataset.get("downloads", 0),
            "likes": dataset.get("likes", 0),
            "tags": dataset.get("tags", []),
            "url": (
                f"https://huggingface.co/datasets/{dataset_id}"
                if dataset_id else ""
            ),
            "source": "Hugging Face"
        })

    return results


def get_dataset_details(dataset_id: str):
    url = f"https://huggingface.co/api/datasets/{dataset_id}"

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    data = response.json()

    return {
        "id": data.get("id"),
        "author": data.get("author"),
        "description": data.get("description") or "",
        "downloads": data.get("downloads", 0),
        "likes": data.get("likes", 0),
        "tags": data.get("tags", []),
        "created_at": data.get("createdAt"),
        "last_modified": data.get("lastModified"),
    }


def search_all_datasets(query: str, limit: int = 10):
    huggingface_results = search_huggingface_datasets(query, limit)

    try:
        kaggle_results = search_kaggle_datasets(query, limit)
    except Exception as e:
        print(f"Kaggle search failed: {e}")
        kaggle_results = []

    for dataset in kaggle_results:
        dataset["source"] = "Kaggle"

    return huggingface_results + kaggle_results
