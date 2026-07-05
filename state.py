from typing import TypedDict

class ArchiveState(TypedDict):
    query: str

    entity: str
    object_type: str
    intent: str

    preferred_sources: list

    source: str
    url: str

    raw_text: str

    docs: list

    answer: str