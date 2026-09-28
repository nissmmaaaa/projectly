from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.paper_service import search_all_papers
from retrieval.paper_retriever import retrieve_papers
from services.dataset_service import (
    search_all_datasets,
    get_dataset_details,
)
from retrieval.dataset_retriever import retrieve_datasets
app = FastAPI(title="Projectly API")

# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/datasets/{dataset_id:path}")
def dataset_details(dataset_id: str):
    return get_dataset_details(dataset_id)
@app.get("/")
def home():
    return {
        "message": "Projectly backend is running",
        "status": "success"
    }
@app.get("/datasets")
def search_datasets(query: str):
    datasets = search_all_datasets(query)

    ranked_datasets = retrieve_datasets(
        project_idea=query,
        datasets=datasets,
        top_k=5
    )

    return ranked_datasets


@app.get("/papers")
def search_papers(query: str):
    papers = search_all_papers(query)

    ranked_papers = retrieve_papers(
        project_idea=query,
        papers=papers,
        top_k=5
    )

    return ranked_papers