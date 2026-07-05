from rag.vectorstore import vector_store

def archive_check_node(state):

    existing = vector_store.get(
        where={"entity": state["entity"]}
    )

    state["archive_exists"] = len(existing["ids"]) > 0

    if state["archive_exists"]:
        print(f"{state['entity']} already exists in archive.")
    else:
        print(f"{state['entity']} not found in archive.")

    return state