import json
from services.gemini_service import generate_response


def understand_project(project_idea: str):

    prompt = f"""
You are the Project Understanding Agent for Projectly.

Analyze the following project idea:

{project_idea}

Return ONLY valid JSON with these fields:

{{
    "domain": "",
    "task": "",
    "data_type": "",
    "keywords": [],
    "technologies": [],
    "dataset_queries": [],
    "paper_queries": [],
    "github_queries": [],
    "resource_queries": []
}}

Rules:
- Understand the actual project requirements.
- Keep queries specific to the project.
- Do not invent unnecessary technologies.
- Return only JSON.
"""

    response = generate_response(prompt)

    response = response.strip()

    if response.startswith("```"):
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

    result = json.loads(response)

    result.setdefault("domain", "")
    result.setdefault("task", "")
    result.setdefault("data_type", "")
    result.setdefault("keywords", [])
    result.setdefault("technologies", [])
    result.setdefault("dataset_queries", [])
    result.setdefault("paper_queries", [])
    result.setdefault("github_queries", [])
    result.setdefault("resource_queries", [])

    return result