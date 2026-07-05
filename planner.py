import json
from typing import List
from pydantic import BaseModel, ValidationError


class Plan(BaseModel):
    entity: str
    object_type: str
    intent: str
    preferred_sources: List[str]


def planner_agent(user_query, llm):

    prompt = f"""
You are the Planning Agent for Celestia Probe.

Your ONLY job is to analyze the user's request.

Do NOT answer the question.

Determine:

1. entity
2. object_type
3. intent
4. preferred_sources

Intent must be one of:

overview
location
atmosphere
surface
structure
formation
temperature
habitability
mission
comparison
other

Object types:

Planet
Moon
Nebula
Galaxy
Black Hole
Star
Constellation
Asteroid
Comet
Spacecraft
Unknown

Source selection rules:

Planets -> NASA then Wikipedia
Moons -> NASA then Wikipedia
Spacecraft -> NASA then Wikipedia

Nebulae -> Wikipedia then NASA
Galaxies -> Wikipedia then NASA
Black Holes -> Wikipedia then NASA
Stars -> Wikipedia then NASA
Constellations -> Wikipedia then NASA

Return ONLY valid JSON.

Example:

{{
    "entity": "Mars",
    "object_type": "Planet",
    "intent": "overview",
    "preferred_sources": ["NASA", "Wikipedia"]
}}

User Query:
{user_query}
"""

    planner_llm = llm.bind(format="json")

    response = planner_llm.invoke(prompt)

    try:
        data = json.loads(response.content)

        plan = Plan(**data)

        return plan.model_dump()

    except (json.JSONDecodeError, ValidationError) as e:
        print("Planner output:", response.content)
        raise RuntimeError(f"Planner failed: {e}")