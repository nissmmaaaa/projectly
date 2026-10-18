from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.paper_service import search_all_papers
from retrieval.paper_retriever import retrieve_papers
from services.dataset_service import (
    search_all_datasets,
    get_dataset_details,
)
from retrieval.dataset_retriever import retrieve_datasets
from services.github_service import search_github_repositories
from retrieval.github_retriever import retrieve_github_repositories
from services.resource_service import search_all_resources
from retrieval.resource_retriever import retrieve_resources
from agents.project_graph import project_graph
from agents.project_analysis_agent import analyze_project

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

@app.get("/github")
def search_github(query: str):
    repositories = search_github_repositories(query)

    ranked_repositories = retrieve_github_repositories(
        project_idea=query,
        repositories=repositories,
        top_k=5
    )

    return ranked_repositories

@app.get("/resources")
def search_resources(query: str):
    resources = search_all_resources(query)

    ranked_resources = retrieve_resources(
        project_idea=query,
        resources=resources,
        top_k=5
    )

    return ranked_resources

@app.get("/understand-project")
def understand_project_endpoint(query: str):
    result = project_graph.invoke({
        "project_idea": query
    })

    return result["understanding"]
@app.get("/project-search")
def project_search(query: str):
    result = project_graph.invoke({
        "project_idea": query
    })

    return {
        "project_idea": query,
        "understanding": result["understanding"],
        "datasets": result["datasets"],
        "papers": result["papers"],
        "github": result["github"],
        "resources": result["resources"]
    }

@app.get("/project-analysis")
def project_analysis(query: str):
    result = project_graph.invoke({
        "project_idea": query
    })

    analysis = analyze_project(
        project_idea=query,
        understanding=result["understanding"],
        datasets=result["datasets"],
        papers=result["papers"],
        github=result["github"]
    )

    return analysis