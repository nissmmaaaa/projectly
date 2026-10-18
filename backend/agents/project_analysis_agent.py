
import json
from services.gemini_service import generate_response



def analyze_project(project_idea, understanding, datasets, papers, github):
    prompt = f"""
You are Projectly's AI Project Analysis Agent.

Project idea: {project_idea}

Project understanding:
{json.dumps(understanding, ensure_ascii=False)}

Available datasets:
{json.dumps(datasets[:3], ensure_ascii=False)}

Research papers:
{json.dumps(papers[:3], ensure_ascii=False)}

GitHub repositories:
{json.dumps(github[:3], ensure_ascii=False)}

Return a JSON object with exactly these fields:
{{
  "project_overview": "string",
  "recommended_technologies": ["string"],
  "roadmap": [
    {{
      "phase": "string",
      "tasks": ["string"]
    }}
  ],
  "feasibility": {{
    "difficulty": "Beginner, Intermediate, or Advanced",
    "estimated_duration": "string",
    "challenges": ["string"],
    "solutions": ["string"]
  }}
}}

Return valid JSON only. Use double quotes for all keys and strings.
Do not include Markdown fences or comments.
Do not add trailing commas.
"""

    response = generate_response(prompt).strip()

    # Remove Markdown code fences if Gemini includes them.
    if response.startswith("```"):
        response = response.replace("```json", "", 1)
        response = response.replace("```", "").strip()

    try:
        result = json.loads(response)
    except json.JSONDecodeError:
        # Retry once with a JSON-repair instruction.
        repair_prompt = f"""
Convert the following content into valid JSON matching this structure:
{{
  "project_overview": "string",
  "recommended_technologies": ["string"],
  "roadmap": [{{"phase": "string", "tasks": ["string"]}}],
  "feasibility": {{
    "difficulty": "string",
    "estimated_duration": "string",
    "challenges": ["string"],
    "solutions": ["string"]
  }}
}}

Return only valid JSON. Do not invent missing information.
Content to repair:
{response}
"""
        repaired = generate_response(repair_prompt).strip()

        if repaired.startswith("```"):
            repaired = repaired.replace("```json", "", 1)
            repaired = repaired.replace("```", "").strip()

        result = json.loads(repaired)

    return result
