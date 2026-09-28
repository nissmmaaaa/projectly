from kaggle.api.kaggle_api_extended import KaggleApi


def search_kaggle_datasets(query: str, limit: int = 10):
    api = KaggleApi()
    api.authenticate()

    datasets = api.dataset_list(
        search=query,
        page=1
    )

    results = []

    for dataset in datasets[:limit]:
        results.append({
            "id": dataset.ref,
            "title": dataset.title,
            "description": dataset.subtitle or "",
            "downloads": dataset.download_count,
            "votes": dataset.vote_count,
            "url": f"https://www.kaggle.com/datasets/{dataset.ref}"
        })

    return results