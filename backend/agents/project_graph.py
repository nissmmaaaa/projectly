from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.project_understanding_agent import understand_project

from services.dataset_service import search_all_datasets
from retrieval.dataset_retriever import retrieve_datasets

from services.paper_service import search_all_papers
from retrieval.paper_retriever import retrieve_papers

from services.github_service import search_github_repositories
from retrieval.github_retriever import retrieve_github_repositories

from services.resource_service import search_all_resources
from retrieval.resource_retriever import retrieve_resources


class ProjectState(TypedDict):
    project_idea: str
    understanding: dict
    datasets: list
    papers: list
    github: list
    resources: list


def understand_node(state: ProjectState):
    result = understand_project(state["project_idea"])

    return {
        "understanding": result
    }



def dataset_node(state: ProjectState):
    understanding = state["understanding"]
    queries = understanding.get("dataset_queries", [])

    if not queries:
        queries = [state["project_idea"]]

    all_datasets = []
    seen_datasets = set()

    for query in queries:
        try:
            datasets = search_all_datasets(query, limit=10)
        except Exception as e:
            print(f"Dataset search failed for '{query}': {e}")
            continue

        for dataset in datasets:
            dataset_id = dataset.get("id")

            if dataset_id and dataset_id not in seen_datasets:
                seen_datasets.add(dataset_id)
                all_datasets.append(dataset)

    ranked_datasets = retrieve_datasets(
        project_idea=state["project_idea"],
        datasets=all_datasets,
        top_k=5
    )

    return {
        "datasets": ranked_datasets
    }



def paper_node(state: ProjectState):
    understanding = state["understanding"]

    queries = understanding.get("paper_queries", [])
    query = " ".join(queries)

    papers = search_all_papers(query)

    ranked_papers = retrieve_papers(
        project_idea=state["project_idea"],
        papers=papers,
        top_k=5
    )

    return {
        "papers": ranked_papers
    }


def github_node(state: ProjectState):
    understanding = state["understanding"]

    queries = understanding.get("github_queries", [])

    all_repositories = []
    seen_repositories = set()

    for query in queries:
        repositories = search_github_repositories(
            query=query,
            limit=10
        )

        for repository in repositories:
            name = repository.get("name")

            if name and name not in seen_repositories:
                seen_repositories.add(name)
                all_repositories.append(repository)

    ranked_repositories = retrieve_github_repositories(
        project_idea=state["project_idea"],
        repositories=all_repositories,
        top_k=5
    )

    return {
        "github": ranked_repositories
    }



def resource_node(state: ProjectState):
    understanding = state["understanding"]
    queries = understanding.get("resource_queries", [])

    if not queries:
        queries = [state["project_idea"]]

    all_resources = []
    seen_urls = set()

    for query in queries:
        try:
            resources = search_all_resources(query, limit=10)
        except Exception as e:
            print(f"Resource search failed for '{query}': {e}")
            continue

        for resource in resources:
            url = resource.get("url")

            if url and url not in seen_urls:
                seen_urls.add(url)
                all_resources.append(resource)

    ranked_resources = retrieve_resources(
        project_idea=state["project_idea"],
        resources=all_resources,
        top_k=5
    )

    return {
        "resources": ranked_resources
    }



graph = StateGraph(ProjectState)

graph.add_node("understand_project", understand_node)
graph.add_node("search_datasets", dataset_node)
graph.add_node("search_papers", paper_node)
graph.add_node("search_github", github_node)
graph.add_node("search_resources", resource_node)

graph.set_entry_point("understand_project")

graph.add_edge("understand_project", "search_datasets")
graph.add_edge("search_datasets", "search_papers")
graph.add_edge("search_papers", "search_github")
graph.add_edge("search_github", "search_resources")
graph.add_edge("search_resources", END)

project_graph = graph.compile()