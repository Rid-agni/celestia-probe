from rag.vectorstore import vector_store


def retrieve(entity, query, k=6):

    docs = vector_store.similarity_search(
        query,
        k=k,
        filter={
            "entity": entity
        }
    )

    return docs