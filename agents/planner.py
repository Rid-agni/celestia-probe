from planner import planner_agent
from config import llm

def planner_node(state):

    plan = planner_agent(
        state["query"],
        llm
    )

    state["entity"] = plan["entity"]
    state["object_type"] = plan["object_type"]
    state["intent"] = plan["intent"]
    state["preferred_sources"] = plan["preferred_sources"]

    return state