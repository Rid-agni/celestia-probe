from typing import TypedDict, List

class ArchiveState(TypedDict):
    query: str

    entity: str
    object_type: str
    intent: str

    preferred_sources: List[str]

    archive_exists: bool

    source: str
    url: str

    raw_text: str

    docs: list
    context: str
    answer: str
    archive_url: str