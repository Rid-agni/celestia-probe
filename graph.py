from langgraph.graph import StateGraph, END
from agents.planner import planner_node
from state import ArchiveState
from agents.archive_check import archive_check_node

builder = StateGraph(ArchiveState)

builder.add_node("planner", planner_node)
builder.add_node(
    "archive_check",
    archive_check_node
)

builder.set_entry_point("planner")

builder.add_edge(
    "planner",
    "archive_check"
)
builder.add_edge(
    "archive_check",
    END
)

graph = builder.compile()