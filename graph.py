from langgraph.graph import StateGraph, END
from agents.planner import planner_node
from state import ArchiveState
from agents.archive_check import archive_check_node
from agents.acquisition import acquisition_node
from agents.retrieval import retrieval_node
from agents.response import response_node

builder = StateGraph(ArchiveState)

builder.add_node("planner", planner_node)
builder.add_node(
    "archive_check",
    archive_check_node
)
builder.add_node(
    "acquisition",
    acquisition_node
)
builder.add_node(
    "retrieval",
    retrieval_node
)
builder.add_node(
    "response",
    response_node
)
builder.set_entry_point("planner")

builder.add_edge(
    "planner",
    "archive_check"
)
builder.add_conditional_edges(
    "archive_check",
    lambda state: (
        "retrieval"
        if state["archive_exists"]
        else "acquisition"
    ),
    {
        "retrieval": "retrieval",
        "acquisition": "acquisition"
    }
)
builder.add_edge(
    "acquisition",
    "retrieval"
)
builder.add_edge(
    "retrieval",
    "response"
)

builder.add_edge(
    "response",
    END
)

graph = builder.compile()