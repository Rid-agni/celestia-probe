from langgraph.graph import StateGraph, END
from agents.planner import planner_node
from state import ArchiveState

builder = StateGraph(ArchiveState)

builder.add_node("planner", planner_node)

builder.set_entry_point("planner")

builder.add_edge(
    "planner",
    END
)

graph = builder.compile()