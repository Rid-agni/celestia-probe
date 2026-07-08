from rag.retrieval import retrieve


def retrieval_node(state):
    
    print("=" * 60)
    print("ENTERED RETRIEVAL NODE")
    print("=" * 60)
    docs = retrieve(
        entity=state["entity"],
        query=state["query"]
    )

    state["docs"] = docs

    if docs:
        state["source"] = docs[0].metadata.get("source", "Unknown")
        state["archive_url"] = docs[0].metadata.get("url", "")

    else:
        state["source"] = "Unknown"
        state["archive_url"] = ""

    return state